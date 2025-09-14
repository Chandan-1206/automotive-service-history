import mysql.connector  # type: ignore

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="test",
        database="automotive_db"
    )

# ---------------- VEHICLES ----------------
def add_vehicle(vin, plate, model, year, owner, contact):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO vehicles (vin, license_plate, model, year, owner_name, owner_contact)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (vin, plate, model, year, owner, contact))
    conn.commit()
    cursor.close()
    conn.close()

def view_vehicles():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, vin, license_plate, model, year, owner_name, owner_contact FROM vehicles")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_vehicle_by_id(vehicle_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vehicles WHERE id=%s", (vehicle_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def update_vehicle(vehicle_id, vin, plate, model, year, owner, contact):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE vehicles
        SET vin=%s, license_plate=%s, model=%s, year=%s, owner_name=%s, owner_contact=%s
        WHERE id=%s
    """, (vin, plate, model, year, owner, contact, vehicle_id))
    conn.commit()
    cursor.close()
    conn.close()


def delete_vehicle(vehicle_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vehicles WHERE id=%s", (vehicle_id,))
    conn.commit()
    cursor.close()
    conn.close()

# ---------------- EMPLOYEES ----------------
def verify_employee(employee_id, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employees WHERE employee_id=%s AND password=%s", (employee_id, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# ---------------- CUSTOMERS ----------------
def verify_customer(owner_name, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vehicles WHERE owner_name=%s AND password=%s", (owner_name, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user
