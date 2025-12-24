import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="yourpassword",      # replace with your MySQL root password
            database="automotive_db"
        )
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# ---------------- VEHICLES ----------------
def add_vehicle(vin, plate, model, year, owner, contact, password, mileage=0):
    conn = get_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    try:
        # Try to insert with mileage column
        cursor.execute("""
            INSERT INTO vehicles (vin, license_plate, model, year, owner_name, owner_contact, password, mileage)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (vin, plate, model, year, owner, contact, password, mileage))
        conn.commit()
        return True
    except Error as e:
        # If mileage column doesn't exist, try without it
        if "Unknown column 'mileage'" in str(e):
            try:
                cursor.execute("""
                    INSERT INTO vehicles (vin, license_plate, model, year, owner_name, owner_contact, password)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (vin, plate, model, year, owner, contact, password))
                conn.commit()
                print("Note: Added vehicle without mileage. Run: ALTER TABLE vehicles ADD COLUMN mileage INT DEFAULT 0;")
                return True
            except Error as e2:
                print(f"Error adding vehicle: {e2}")
                return False
        else:
            print(f"Error adding vehicle: {e}")
            return False
    finally:
        cursor.close()
        conn.close()

def view_vehicles():
    conn = get_connection()
    if conn is None:
        return []
        
    cursor = conn.cursor(dictionary=True, buffered=True)
    try:
        cursor.execute("SELECT id, vin, license_plate, model, year, owner_name, owner_contact FROM vehicles")
        return cursor.fetchall()
    except Error as e:
        print(f"Error fetching vehicles: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_customer_vehicles(owner_name):
    """Get vehicles for a specific customer only"""
    conn = get_connection()
    if conn is None:
        return []
        
    cursor = conn.cursor(dictionary=True, buffered=True)
    try:
        cursor.execute("""
            SELECT id, vin, license_plate, model, year, owner_name, owner_contact 
            FROM vehicles 
            WHERE owner_name=%s
        """, (owner_name,))
        return cursor.fetchall()
    except Error as e:
        print(f"Error fetching customer vehicles: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def search_vehicle_by_vin(vin):
    """Search for a vehicle by VIN (public access)"""
    conn = get_connection()
    if conn is None:
        return None
        
    cursor = conn.cursor(dictionary=True, buffered=True)
    try:
        cursor.execute("""
            SELECT id, vin, license_plate, model, year, owner_name, owner_contact 
            FROM vehicles 
            WHERE vin=%s
        """, (vin,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error searching vehicle by VIN: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_vehicle_by_id(vehicle_id):
    conn = get_connection()
    if conn is None:
        return None
        
    cursor = conn.cursor(dictionary=True, buffered=True)
    try:
        cursor.execute("SELECT * FROM vehicles WHERE id=%s", (vehicle_id,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error fetching vehicle: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def update_vehicle(vehicle_id, vin, plate, model, year, owner, contact, password=None):
    conn = get_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    try:
        if password:  # Update password if provided
            cursor.execute("""
                UPDATE vehicles
                SET vin=%s, license_plate=%s, model=%s, year=%s, owner_name=%s, owner_contact=%s, password=%s
                WHERE id=%s
            """, (vin, plate, model, year, owner, contact, password, vehicle_id))
        else:  # Don't update password if not provided
            cursor.execute("""
                UPDATE vehicles
                SET vin=%s, license_plate=%s, model=%s, year=%s, owner_name=%s, owner_contact=%s
                WHERE id=%s
            """, (vin, plate, model, year, owner, contact, vehicle_id))
        conn.commit()
        return True
    except Error as e:
        print(f"Error updating vehicle: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_vehicle(vehicle_id):
    conn = get_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM vehicles WHERE id=%s", (vehicle_id,))
        conn.commit()
        return True
    except Error as e:
        print(f"Error deleting vehicle: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

# ---------------- EMPLOYEES ----------------
def verify_employee(employee_id, password):
    conn = get_connection()
    if conn is None:
        return None
        
    cursor = conn.cursor(dictionary=True, buffered=True)
    try:
        cursor.execute("SELECT * FROM employees WHERE employee_id=%s AND password=%s", (employee_id, password))
        return cursor.fetchone()
    except Error as e:
        print(f"Error verifying employee: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# ---------------- CUSTOMERS ----------------
def verify_customer(owner_name, password):
    conn = get_connection()
    if conn is None:
        return None
        
    cursor = conn.cursor(dictionary=True, buffered=True)
    try:
        cursor.execute("SELECT * FROM vehicles WHERE owner_name=%s AND password=%s", (owner_name, password))
        return cursor.fetchone()
    except Error as e:
        print(f"Error verifying customer: {e}")
        return None
    finally:
        cursor.close()
        conn.close()