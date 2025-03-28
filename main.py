# Import the initialization function and CRUD classes
from create_database_if_not_exist import initialize_database
from crud import Species, Animals, FoodTypes, FoodInventory, Roles, Staff, Feeding


def populate_database():
    """
    Populate the database with sample data to demonstrate the Zoo Management System
    """
    try:
        # Initialize the database (this will reset it if it already exists)
        initialize_database(force_new=False) # Switch to "TRUE" if you wish to regenarate database
        print("Database initialized successfully!")

        # 1. Create Species
        species_methods = [
            ("African Lion", "Savanna", "Carnivore"),
            ("African Elephant", "Grassland", "Herbivore"),
            ("Emperor Penguin", "Antarctic", "Piscivore"),
            ("Reticulated Giraffe", "Savanna", "Herbivore")
        ]
        species_ids = []
        for name, habitat, diet in species_methods:
            species_id = Species.create(name, habitat, diet)
            species_ids.append(species_id)
            print(f"Created Species: {name} (ID: {species_id})")

        # 2. Add Animals
        animal_methods = [
            ("Simba", species_ids[0], "Male", "2015-03-15", "Healthy"),
            ("Nala", species_ids[0], "Female", "2016-05-20", "Healthy"),
            ("Dumbo", species_ids[1], "Male", "2010-07-10", "Good"),
            ("Tux", species_ids[2], "Male", "2018-12-01", "Active"),
            ("Patches", species_ids[3], "Female", "2017-09-25", "Good")
        ]
        animal_ids = []
        for name, species_id, gender, birthdate, health_status in animal_methods:
            animal_id = Animals.create(name, species_id, gender, birthdate, health_status)
            animal_ids.append(animal_id)
            print(f"Created Animal: {name} (ID: {animal_id})")

        # 3. Create Food Types
        food_methods = [
            ("Raw Meat", "kg", "Refrigerated"),
            ("Hay", "kg", "Dry storage"),
            ("Frozen Fish", "kg", "Freezer"),
            ("Mixed Fruits", "kg", "Refrigerated")
        ]
        food_ids = []
        for name, unit, storage in food_methods:
            food_id = FoodTypes.create(name, unit, storage)
            food_ids.append(food_id)
            print(f"Created Food Type: {name} (ID: {food_id})")

        # 4. Add Food Inventory
        inventory_methods = [
            (food_ids[0], 500.0, "2024-12-31"),
            (food_ids[1], 1000.0, "2024-11-15"),
            (food_ids[2], 250.0, "2024-10-30"),
            (food_ids[3], 300.0, "2024-09-15")
        ]
        inventory_ids = []
        for food_type_id, quantity, expiration_date in inventory_methods:
            inventory_id = FoodInventory.create(food_type_id, quantity, expiration_date)
            inventory_ids.append(inventory_id)
            print(f"Created Food Inventory: Type ID {food_type_id} (Inventory ID: {inventory_id})")

        # 5. Create Staff Roles
        role_methods = [
            ("Zookeeper", "Animal Care", "Responsible for daily animal care"),
            ("Veterinarian", "Medical", "Provides medical care"),
            ("Zoo Manager", "Administration", "Oversees zoo operations")
        ]
        role_ids = []
        for title, department, description in role_methods:
            role_id = Roles.create(title, department, description)
            role_ids.append(role_id)
            print(f"Created Role: {title} (ID: {role_id})")

        # 6. Add Staff
        staff_methods = [
            ("John", "Smith", role_ids[0], "USA", 50000),
            ("Maria", "Garcia", role_ids[1], "Spain", 75000),
            ("Alex", "Wong", role_ids[2], "Canada", 90000)
        ]
        staff_ids = []
        for first_name, last_name, role_id, country, salary in staff_methods:
            staff_id = Staff.create(first_name, last_name, role_id, country, salary)
            staff_ids.append(staff_id)
            print(f"Created Staff: {first_name} {last_name} (ID: {staff_id})")

        # 7. Record Feedings
        feeding_methods = [
            (animal_ids[0], food_ids[0], staff_ids[0], 10.5, "Morning feeding"),
            (animal_ids[2], food_ids[1], staff_ids[0], 25.0, "Midday feeding"),
            (animal_ids[3], food_ids[2], staff_ids[1], 5.2, "Fish diet")
        ]
        feeding_ids = []
        for animal_id, food_type_id, staff_id, quantity, notes in feeding_methods:
            feeding_id = Feeding.create(animal_id, food_type_id, staff_id, quantity, notes)
            feeding_ids.append(feeding_id)
            print(f"Created Feeding Record: Animal ID {animal_id} (Feeding ID: {feeding_id})")

        print("\n--- Database Population Complete ---")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    populate_database()