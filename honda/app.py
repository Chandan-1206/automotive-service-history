from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import crud

app = Flask(__name__)
app.secret_key = "supersecret"  # needed for session login

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")  # choose role

# ---------------- LOGIN ----------------
@app.route("/login/<role>", methods=["GET", "POST"])
def login(role):
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if role == "employee":
            user = crud.verify_employee(username, password)
            if user:
                session["user"] = {"role": "employee", "id": user["id"]}
                return redirect(url_for("employee_dashboard"))
        elif role == "customer":
            user = crud.verify_customer(username, password)
            if user:
                session["user"] = {"role": "customer", "id": user["id"]}
                return redirect(url_for("customer_dashboard"))

        return "❌ Invalid credentials", 401

    return render_template("login.html", role=role)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# ---------------- DASHBOARDS ----------------
@app.route("/customer/dashboard")
def customer_dashboard():
    if "user" not in session or session["user"]["role"] != "customer":
        return redirect(url_for("home"))
    vehicles = crud.view_vehicles()
    return render_template("vehicles.html", vehicles=vehicles, role="customer")

@app.route("/employee/dashboard")
def employee_dashboard():
    if "user" not in session or session["user"]["role"] != "employee":
        return redirect(url_for("home"))
    vehicles = crud.view_vehicles()
    return render_template("vehicles.html", vehicles=vehicles, role="employee")

# ---------------- API for AJAX in CRUD ----------------
@app.route("/vehicles")
def get_vehicles():
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
        crud.add_vehicle(vin, plate, model, year, owner, contact)
        return redirect(url_for("employee_dashboard"))
    return render_template("add.html")

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
        crud.update_vehicle(vehicle_id, vin, plate, model, year, owner, contact)
        return redirect(url_for("employee_dashboard"))

    vehicle = crud.get_vehicle_by_id(vehicle_id)
    return render_template("update.html", vehicle=vehicle)

@app.route("/delete/<int:vehicle_id>")
def delete_vehicle(vehicle_id):
    if "user" not in session or session["user"]["role"] != "employee":
        return redirect(url_for("home"))

    crud.delete_vehicle(vehicle_id)
    return redirect(url_for("employee_dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
