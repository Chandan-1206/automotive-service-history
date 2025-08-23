import mysql.connector

# Connect to database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="test",
    database="automotive_db"
)
cursor = conn.cursor()

def add_vehicle():
    vin = input("Enter VIN: ")
    plate = input("Enter License Plate: ")
    model = input("Enter Model: ")
    year = int(input("Enter Year: "))
    owner = input("Enter Owner Name: ")
    contact = input("Enter Owner Contact: ")

    cursor.execute("""
        INSERT INTO vehicles (vin, license_plate, model, year, owner_name, owner_contact)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (vin, plate, model, year, owner, contact))
    conn.commit()
    print("✅ Vehicle added successfully!\n")

def view_vehicles():
    cursor.execute("SELECT * FROM vehicles")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print()

def update_vehicle():
    vid = input("Enter Vehicle VIN to update: ")
    new_owner = input("Enter new owner name: ")
    cursor.execute("UPDATE vehicles SET owner_name=%s WHERE vin=%s", (new_owner, vid))
    conn.commit()
    print("✅ Vehicle updated successfully!\n")

def delete_vehicle():
    vid = input("Enter Vehicle VIN to delete: ")
    cursor.execute("DELETE FROM vehicles WHERE vin=%s", (vid,))
    conn.commit()
    print("✅ Vehicle deleted successfully!\n")

def menu():
    while True:
        print("\n--- Vehicle Management ---")
        print("1. Add Vehicle")
        print("2. View Vehicles")
        print("3. Update Vehicle Owner")
        print("4. Delete Vehicle")
        print("5. Exit")

        choice = input("Choose option: ")
        if choice == "1":
            add_vehicle()
        elif choice == "2":
            view_vehicles()
        elif choice == "3":
            update_vehicle()
        elif choice == "4":
            delete_vehicle()
        elif choice == "5":
            break
        else:
            print("❌ Invalid choice, try again.")

menu()

cursor.close()
conn.close()
