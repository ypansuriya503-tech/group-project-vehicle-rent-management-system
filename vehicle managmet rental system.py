#group project:-
#project name: vehicle rental management system:-

class Vehicle:

    LATE_FEE_PER_DAY = 200

    def __init__(self, vehicle_id, brand, model, rental_price_per_day,
                 availability_status=True, renter_id=None):
        self.vehicle_id = vehicle_id
        self.brand = brand
        self.model = model
        self.__rental_price_per_day = rental_price_per_day
        self.__availability_status = availability_status
        self.__renter_id = renter_id

    def get_rental_price_per_day(self):
        return self.__rental_price_per_day

    def set_rental_price_per_day(self, price):
        if price <= 0:
            print("Rental price must be greater than 0.")
            return
        self.__rental_price_per_day = price

    def get_availability_status(self):
        return self.__availability_status

    def set_availability_status(self, status):
        self.__availability_status = bool(status)

    def get_renter_id(self):
        return self.__renter_id

    def set_renter_id(self, renter_id):
        self.__renter_id = renter_id

    def display(self):
        status = "Available" if self.__availability_status else "Rented"
        print(f"ID: {self.vehicle_id}")
        print(f"Brand: {self.brand}")
        print(f"Model: {self.model}")
        print(f"Rental Price/Day: Rs. {self.__rental_price_per_day:.2f}")
        print(f"Availability: {status}")
        if self.__renter_id is not None:
            print(f"Renter ID: {self.__renter_id}")


class Car(Vehicle):
    def __init__(self, vehicle_id, brand, model, rental_price_per_day,
                 number_of_seats, fuel_type,
                 availability_status=True, renter_id=None):
        super().__init__(
            vehicle_id, brand, model, rental_price_per_day,
            availability_status, renter_id
        )
        self.number_of_seats = number_of_seats
        self.fuel_type = fuel_type

    def display(self):
        print("\n--- Car Details ---")
        super().display()
        print(f"Number of Seats: {self.number_of_seats}")
        print(f"Fuel Type: {self.fuel_type}")


class Bike(Vehicle):
    def __init__(self, vehicle_id, brand, model, rental_price_per_day,
                 bike_type, availability_status=True, renter_id=None):
        super().__init__(
            vehicle_id, brand, model, rental_price_per_day,
            availability_status, renter_id
        )
        self.bike_type = bike_type

    def display(self):
        print("\n--- Bike Details ---")
        super().display()
        print(f"Bike Type: {self.bike_type}")


class VehicleFactory:
    def create_basic(vehicle_id, brand, model, price):
        return Vehicle(vehicle_id, brand, model, price)

    def create_available(vehicle_id, brand, model, price):
        return Vehicle(vehicle_id, brand, model, price, True)


vehicles = {}
next_vehicle_id = 1


def get_int(prompt, minimum=1):
        value = int(input(prompt))
        if value < minimum:
            print(f"Value must be at least {minimum}.")
            return None
        return value
        return None


def get_float(prompt, minimum=0):
        value = float(input(prompt))
        if value < minimum:
            print(f"Value must be at least {minimum}.")
            return None
        return value


def add_car():
    global next_vehicle_id

    print("\n--- Add a Car ---")
    brand = input("Enter car brand: ").strip()
    model = input("Enter car model: ").strip()
    price = get_float("Enter rental price per day: Rs. ", 1)
    seats = get_int("Enter number of seats: ", 1)

    if price is None or seats is None:
        return

    fuel_type = input("Enter fuel type (Petrol/Diesel/Electric/CNG): ").strip()

    car = Car(
        next_vehicle_id, brand, model, price,
        seats, fuel_type
    )
    vehicles[next_vehicle_id] = car

    print(f"Car added successfully with Vehicle ID: {next_vehicle_id}")
    next_vehicle_id += 1


def add_bike():
    global next_vehicle_id

    print("\n--- Add a Bike ---")
    brand = input("Enter bike brand: ").strip()
    model = input("Enter bike model: ").strip()
    price = get_float("Enter rental price per day: Rs. ", 1)

    if price is None:
        return

    bike_type = input(
        "Enter bike type (Cruiser/Sports/Standard): "
    ).strip()

    bike = Bike(
        next_vehicle_id, brand, model, price,
        bike_type
    )
    vehicles[next_vehicle_id] = bike

    print(f"Bike added successfully with Vehicle ID: {next_vehicle_id}")
    next_vehicle_id += 1


def show_vehicle_details():
    if not vehicles:
        print("\nNo vehicles available in the system.")
        return

    print("\n========== ALL VEHICLES ==========")
    for vehicle in vehicles.values():
        vehicle.display()
        print("-" * 35)


def rent_vehicle():
    if not vehicles:
        print("\nNo vehicles have been added yet.")
        return

    vehicle_id = get_int("Enter Vehicle ID to rent: ")
    if vehicle_id is None or vehicle_id not in vehicles:
        print("Vehicle ID not found.")
        return

    vehicle = vehicles[vehicle_id]

    if not vehicle.get_availability_status():
        print("Sorry, this vehicle is already rented.")
        return

    renter_id = input("Enter renter ID: ").strip()
    if not renter_id:
        print("Renter ID cannot be empty.")
        return

    days = get_int("Enter number of rental days: ", 1)
    if days is None:
        return

    total = vehicle.get_rental_price_per_day() * days
    minimum_advance = total * 0.30

    print(f"Total Rent: Rs. {total:.2f}")
    print(f"Minimum Advance (30%): Rs. {minimum_advance:.2f}")

    advance = float(input("Enter advance payment: Rs. "))

    if advance < minimum_advance:
        print("Advance must be at least 30% of total rent.")
        return

    if advance > total:
        print("Advance cannot be greater than total rent.")
        return

    vehicle.set_availability_status(False)
    vehicle.set_renter_id(renter_id)

    print("\nVehicle rented successfully!")
    print(f"Balance to pay: Rs. {total - advance:.2f}")


def return_vehicle():
    vehicle_id = get_int("Enter Vehicle ID to return: ")
    if vehicle_id is None or vehicle_id not in vehicles:
        print("Vehicle ID not found.")
        return

    vehicle = vehicles[vehicle_id]

    if vehicle.get_availability_status():
        print("This vehicle is not currently rented.")
        return

    vehicle.set_availability_status(True)
    vehicle.set_renter_id(None)

    print("Vehicle returned successfully.")
    print(f"Late fee rule: Rs. {Vehicle.LATE_FEE_PER_DAY} per extra day.")


def demonstrate_instanceof():
    if not vehicles:
        print("\nNo vehicles available.")
        return

    print("\n--- isinstance() Demonstration ---")
    for vehicle in vehicles.values():
        if isinstance(vehicle, Car):
            print(f"Vehicle {vehicle.vehicle_id} is a Car.")
        elif isinstance(vehicle, Bike):
            print(f"Vehicle {vehicle.vehicle_id} is a Bike.")
        else:
            print(f"Vehicle {vehicle.vehicle_id} is a Vehicle.")


def show_menu():
    print("""
---------- VEHICLE RENTAL SYSTEM ---------
1. Add a Car
2. Add a Bike
3. Rent a Vehicle
4. Return a Vehicle
5. Show Vehicle Details
6. Demonstrate isinstance()
7. Exit
""")


def main():
    print("Welcome to the Vehicle Rental Management System!")

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_car()
        elif choice == "2":
            add_bike()
        elif choice == "3":
            rent_vehicle()
        elif choice == "4":
            return_vehicle()
        elif choice == "5":
            show_vehicle_details()
        elif choice == "6":
            demonstrate_instanceof()
        elif choice == "7":
            print("Thank you for using the Vehicle Rental System.")
            break
        else:
            print("Invalid choice. Please select 1 to 7.")


if __name__ == "__main__":
    main()
