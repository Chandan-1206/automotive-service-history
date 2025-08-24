import crud

def menu():
    while True:
        print("\n--- Vehicle Management ---")
        print("1. Add Vehicle")
        print("2. View Vehicles")
        print("3. Update Vehicle")
        print("4. Delete Vehicle")
        print("5. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            vin = input("VIN: ")
            plate = input("License Plate: ")
            model = input("Model: ")
            year = int(input("Year: "))
            owner = input("Owner Name: ")
            contact = input("Owner Contact: ")
            crud.add_vehicle(vin, plate, model, year, owner, contact)

        elif choice == "2":
            vehicles = crud.view_vehicles()
            for v in vehicles:
                print(v)

        elif choice == "3":
            vin = input("Enter VIN to update: ")
            field = input("Field to update (license_plate/model/year/owner_name/owner_contact): ")
            new_value = input("New value: ")
            crud.update_vehicle(vin, field, new_value)

        elif choice == "4":
            vin = input("Enter VIN to delete: ")
            crud.delete_vehicle(vin)

        elif choice == "5":
            break

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    menu()
