#dbsetup.py

import mysql.connector
import random
from datetime import datetime

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword"  # replace with your MySQL root password
    )

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Reset DB
    cursor.execute("DROP DATABASE IF EXISTS automotive_db")
    cursor.execute("CREATE DATABASE automotive_db")
    cursor.execute("USE automotive_db")

    # Vehicles table (with mileage)
    cursor.execute("""
        CREATE TABLE vehicles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            vin VARCHAR(100),
            license_plate VARCHAR(50),
            model VARCHAR(100),
            year INT,
            mileage INT,
            owner_name VARCHAR(100),
            owner_contact VARCHAR(100),
            password VARCHAR(100)
        )
    """)

    # Employees table
    cursor.execute("""
        CREATE TABLE employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            employee_id VARCHAR(50) UNIQUE,
            password VARCHAR(100) NOT NULL
        )
    """)

    # Sample pools
    owner_names = ["Ramesh", "Suresh", "Meena", "Anjali", "Vikram", "Priya", "Amit", "Neha", "Arjun", "Kavita"]
    sirnames = ["Garg", "Sharma", "Agarwal", "Rai", "Bharadwaj", "Vashishth", "Gupta", "Goyal", "Panwar", "Singhal"]
    car_models = [
        "Honda Amaze", "Honda Jazz", "Honda Civic", "Honda WR-V",
        "Maruti Celerio", "Ford Mustang", "Mahindra Thar", "Tata Tiago"
    ]
    years = list(range(2015, 2024))

    current_year = datetime.now().year

    # Generate 50 random vehicles
    vehicles = []
    for i in range(50):
        vin = f"VIN{1000+i}"
        plate = f"DL{random.randint(1,99):02d}{random.choice(['AB','XY','PQ','MN'])}{random.randint(1000,9999)}"
        model = random.choice(car_models)
        year = random.choice(years)

        # 🔑 Realistic mileage calculation
        vehicle_age = current_year - year
        mileage = random.randint(
            vehicle_age * 12000,
            vehicle_age * 15000
        )

        owner = random.choice(owner_names) + ' ' + random.choice(sirnames)
        contact = f"9{random.randint(100000000, 999999999)}"
        password = f"pass{i+1}"

        vehicles.append((vin, plate, model, year, mileage, owner, contact, password))

    cursor.executemany("""
        INSERT INTO vehicles
        (vin, license_plate, model, year, mileage, owner_name, owner_contact, password)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, vehicles)

    # Sample employees
    employees = [
        ("EMP001", "admin123"),
        ("EMP002", "emp456"),
        ("EMP003", "secure789"),
        ("EMP004", "admin456"),
        ("EMP005", "emp123")
    ]
    cursor.executemany(
        "INSERT INTO employees (employee_id, password) VALUES (%s, %s)",
        employees
    )

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Database setup complete with mileage included!")

if __name__ == "__main__":
    setup_database()
