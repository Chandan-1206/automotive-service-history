from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import crud
from ml_predictor import ml_system

app = Flask(__name__)
app.secret_key = "supersecret"  # needed for session login

# Load ML model at startup
print("Loading ML model...")
ml_system.load_model()

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- VIN SEARCH (Employee Access Only) ----------------
@app.route("/search", methods=["GET", "POST"])
def search_vehicle():
    # Only allow if user is logged in as employee
    if "user" not in session or session["user"]["role"] != "employee":
        return redirect(url_for("home"))
    
    if request.method == "POST":
        vin = request.form.get("vin", "").strip()
        if vin:
            vehicle = crud.search_vehicle_by_vin(vin)
            if vehicle:
                return render_template("index.html", search_result=vehicle, searched_vin=vin)
            else:
                return render_template("index.html", search_error=f"No vehicle found with VIN: {vin}", searched_vin=vin)
    
    # If GET request, show the search form in employee dashboard
    return redirect(url_for("employee_dashboard"))

# ---------------- VIN SEARCH FROM EMPLOYEE DASHBOARD ----------------
@app.route("/employee/search", methods=["POST"])
def employee_search():
    if "user" not in session or session["user"]["role"] != "employee":
        return redirect(url_for("home"))
    
    vin = request.form.get("vin", "").strip()
    if vin:
        vehicle = crud.search_vehicle_by_vin(vin)
        if vehicle:
            return render_template("index.html", search_result=vehicle, searched_vin=vin)
        else:
            return render_template("index.html", 
                                 search_error=f"No vehicle found with VIN: {vin}", 
                                 searched_vin=vin,
                                 role="employee",
                                 dashboard=True,
                                 employee_id=session["user"]["employee_id"],
                                 vehicles=crud.view_vehicles(),
                                 total_vehicles=len(crud.view_vehicles()))
    
    return redirect(url_for("employee_dashboard"))

# ---------------- LOGIN ----------------
@app.route("/login/<role>", methods=["GET", "POST"])
def login(role):
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if role == "employee":
            user = crud.verify_employee(username, password)
            if user:
                session["user"] = {
                    "role": "employee", 
                    "id": user["id"],
                    "employee_id": user["employee_id"]
                }
                return redirect(url_for("employee_dashboard"))
        elif role == "customer":
            user = crud.verify_customer(username, password)
            if user:
                session["user"] = {
                    "role": "customer", 
                    "id": user["id"],
                    "owner_name": user["owner_name"]
                }
                return redirect(url_for("customer_dashboard"))

        return render_template("index.html", error="Invalid credentials", role=role)
    
    return render_template("index.html", role=role)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# ---------------- DASHBOARDS ----------------
@app.route("/customer/dashboard")
def customer_dashboard():
    if "user" not in session or session["user"]["role"] != "customer":
        return redirect(url_for("home"))
    
    # Get only vehicles owned by this customer
    owner_name = session["user"]["owner_name"]
    vehicles = crud.get_customer_vehicles(owner_name)
    
    # Calculate stats for this customer
    total_vehicles = len(vehicles)
    
    return render_template("index.html", 
                         vehicles=vehicles, 
                         role="customer", 
                         dashboard=True,
                         customer_name=owner_name,
                         total_vehicles=total_vehicles)

@app.route("/employee/dashboard")
def employee_dashboard():
    if "user" not in session or session["user"]["role"] != "employee":
        return redirect(url_for("home"))
    
    vehicles = crud.view_vehicles()
    employee_id = session["user"]["employee_id"]
    
    return render_template("index.html", 
                         vehicles=vehicles, 
                         role="employee", 
                         dashboard=True,
                         employee_id=employee_id,
                         total_vehicles=len(vehicles))

# ---------------- API for AJAX in CRUD ----------------
@app.route("/vehicles")
def get_vehicles():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    if session["user"]["role"] == "customer":
        owner_name = session["user"]["owner_name"]
        data = crud.get_customer_vehicles(owner_name)
    else:
        data = crud.view_vehicles()
    
    return jsonify(data)

# ---------------- VEHICLE CRUD (Employee Only) ----------------
@app.route("/add", methods=["GET", "POST"])
def add_vehicle():
    if "user" not in session or session["user"]["role"] != "employee":
        return redirect(url_for("home"))

    if request.method == "POST":
        vin = request.form["vin"]
        plate = request.form["plate"]
        model = request.form["model"]
        year = request.form["year"]
        owner = request.form["owner"]
        contact = request.form["contact"]
        password = request.form["password"]
        mileage = request.form.get("mileage", 0)
        
        # Get ML predictions
        predicted_issues = ml_system.predict_service_issues(model, year, mileage)
        issue_priorities = ml_system.get_issue_priorities(predicted_issues, 2024 - int(year), int(mileage))
        
        success = crud.add_vehicle(vin, plate, model, year, owner, contact, password, mileage)
        
        if success:
            # Pass predictions to show on dashboard
            return render_template("index.html", 
                                 role="employee",
                                 show_predictions=True,
                                 predicted_issues=predicted_issues,
                                 issue_priorities=issue_priorities,
                                 vehicle_info={
                                     'model': model,
                                     'year': year,
                                     'vin': vin,
                                     'mileage': mileage
                                 })
        else:
            return render_template("index.html", add_vehicle=True, error="Failed to add vehicle")
    
    return render_template("index.html", add_vehicle=True)

@app.route("/update/<int:vehicle_id>", methods=["GET", "POST"])
def update_vehicle(vehicle_id):
    if "user" not in session or session["user"]["role"] != "employee":
        return redirect(url_for("home"))

    if request.method == "POST":
        vin = request.form["vin"]
        plate = request.form["plate"]
        model = request.form["model"]
        year = request.form["year"]
        owner = request.form["owner"]
        contact = request.form["contact"]
        password = request.form.get("password", "")  # Optional password update
        
        success = crud.update_vehicle(vehicle_id, vin, plate, model, year, owner, contact, password)
        
        if success:
            return redirect(url_for("employee_dashboard"))
        else:
            vehicle = crud.get_vehicle_by_id(vehicle_id)
            return render_template("index.html", vehicle=vehicle, update_vehicle=True, error="Failed to update vehicle")

    vehicle = crud.get_vehicle_by_id(vehicle_id)
    return render_template("index.html", vehicle=vehicle, update_vehicle=True)

@app.route("/delete/<int:vehicle_id>")
def delete_vehicle(vehicle_id):
    if "user" not in session or session["user"]["role"] != "employee":
        return redirect(url_for("home"))

    crud.delete_vehicle(vehicle_id)
    return redirect(url_for("employee_dashboard"))

# ---------------- ML PREDICTION API ----------------
@app.route("/predict_issues", methods=["POST"])
def predict_issues():
    """API endpoint to get ML predictions for a vehicle"""
    if "user" not in session or session["user"]["role"] != "employee":
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        data = request.json
        model = data.get('model', '')
        year = data.get('year', 2020)
        mileage = data.get('mileage', 0)
        
        predicted_issues = ml_system.predict_service_issues(model, year, mileage)
        issue_priorities = ml_system.get_issue_priorities(predicted_issues, 2024 - int(year), int(mileage))
        
        return jsonify({
            'success': True,
            'predicted_issues': predicted_issues,
            'priorities': issue_priorities
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)