import mysql.connector # type: ignore

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="test",
        database="automotive_db"
    )

def add_vehicle(vin, plate, model, year, owner, contact):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO vehicles (vin, license_plate, model, year, owner_name, owner_contact)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (vin, plate, model, year, owner, contact))
    conn.commit()
    conn.close()

def view_vehicles():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehicles")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_vehicle(vin, field, new_value):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE vehicles SET {field} = %s WHERE vin = %s", (new_value, vin))
    conn.commit()
    conn.close()

def delete_vehicle(vin):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vehicles WHERE vin = %s", (vin,))
    conn.commit()
    conn.close()
