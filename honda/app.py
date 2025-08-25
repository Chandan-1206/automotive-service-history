from flask import Flask, render_template, request, jsonify, redirect, url_for
import crud

app = Flask(__name__)

# Home page -> list all vehicles
@app.route('/')
def index():
    vehicles = crud.view_vehicles()
    return render_template('index.html', vehicles=vehicles)

# Add vehicle (GET shows form, POST saves data)
@app.route('/add', methods=['GET', 'POST'])
def add_vehicle():
    if request.method == 'POST':
        vin = request.form['vin']
        plate = request.form['plate']
        model = request.form['model']
        year = request.form['year']
        owner = request.form['owner']
        contact = request.form['contact']
        crud.add_vehicle(vin, plate, model, year, owner, contact)
        return redirect(url_for('index'))
    return render_template('add.html')

# Update vehicle
@app.route('/update/<int:vehicle_id>', methods=['GET', 'POST'])
def update_vehicle(vehicle_id):
    if request.method == 'POST':
        vin = request.form['vin']
        plate = request.form['plate']
        model = request.form['model']
        year = request.form['year']
        owner = request.form['owner']
        contact = request.form['contact']
        crud.update_vehicle(vehicle_id, plate, vin, model, year, owner, contact)
        return redirect(url_for('index'))
    vehicle = crud.get_vehicle_by_id(vehicle_id)
    return render_template('update.html', vehicle=vehicle)

# Delete vehicle
@app.route('/delete/<int:vehicle_id>')
def delete_vehicle(vehicle_id):
    crud.delete_vehicle(vehicle_id)
    return redirect(url_for('index'))

# API endpoint
@app.route("/vehicles", methods=["GET"])
def get_vehicles():
    data = crud.view_vehicles()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
