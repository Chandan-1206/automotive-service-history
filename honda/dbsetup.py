import mysql.connector

# Connect to MySQL server (adjust user/pass if needed)
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="test"
)

cursor = conn.cursor()

# Create database if not exists
cursor.execute("CREATE DATABASE IF NOT EXISTS automotive_db")
cursor.execute("USE automotive_db")

# Create Vehicle table
cursor.execute("""
CREATE TABLE IF NOT EXISTS vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vin VARCHAR(50) UNIQUE NOT NULL,
    license_plate VARCHAR(20) UNIQUE,
    model VARCHAR(100),
    year INT,
    owner_name VARCHAR(100),
    owner_contact VARCHAR(50)
)
""")

print("Database and Vehicle table ready.")

# ✅ INSERT DATA
cursor.execute("""
INSERT INTO vehicles (vin, license_plate, model, year, owner_name, owner_contact)
VALUES (%s, %s, %s, %s, %s, %s)
""", ("1HGCM82633A123456", "DL8CAF1234", "Honda City", 2022, "Chandan", "9876543210"))

conn.commit()

# ✅ FETCH DATA BACK
cursor.execute("SELECT * FROM vehicles")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
