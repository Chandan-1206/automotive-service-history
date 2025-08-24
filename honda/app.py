from flask import Flask, render_template, request, redirect, url_for
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
        plate = request.form['plate']
        vin = request.form['vin']
        owner = request.form['owner']
        crud.add_vehicle(plate, vin, owner)
        return redirect(url_for('index'))
    return render_template('add.html')

# Update vehicle
@app.route('/update/<int:vehicle_id>', methods=['GET', 'POST'])
def update_vehicle(vehicle_id):
    if request.method == 'POST':
        plate = request.form['plate']
        vin = request.form['vin']
        owner = request.form['owner']
        crud.update_vehicle(vehicle_id, plate, vin, owner)
        return redirect(url_for('index'))
    vehicle = crud.get_vehicle_by_id(vehicle_id)  # you’ll need this in crud.py
    return render_template('update.html', vehicle=vehicle)

# Delete vehicle
@app.route('/delete/<int:vehicle_id>')
def delete_vehicle(vehicle_id):
    crud.delete_vehicle(vehicle_id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
