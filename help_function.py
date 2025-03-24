def help():
    """
    Displays help information about the Zoo Management System.

    This function provides an overview of the system, database description, and usage examples.

    Returns:
        str: Help text information
    """
    help_text = """
    Zoo Management System
    =====================

    This system provides CRUD (Create, Read, Update, Delete) operations for managing a zoo database.
    The database has a normalized structure (3rd normal form) with transaction support.

    DATABASE STRUCTURE:
    ------------------

    1. Species:
       - speciesID: Unique identifier for species
       - name: Species name
       - habitat: Natural habitat
       - diet: Diet type

    2. Animals:
       - animalID: Unique identifier for animal
       - name: Animal name
       - speciesID: Relationship to Species table
       - gender: Animal gender
       - birthdate: Date of birth
       - health_status: Health condition

    3. FoodTypes:
       - foodTypeID: Unique identifier for food type
       - name: Food type name
       - unit: Unit of measurement
       - storage_requirements: Storage requirements

    4. FoodInventory:
       - inventoryID: Unique identifier for inventory record
       - foodTypeID: Relationship to FoodTypes table
       - quantity: Amount
       - expiration_date: Expiration date
       - last_updated: Last update date

    5. Roles:
       - roleID: Unique identifier for role
       - title: Role title
       - department: Department
       - description: Description

    6. Staff:
       - staffID: Unique identifier for staff member
       - firstName: First name
       - lastName: Last name
       - roleID: Relationship to Roles table
       - country: Country of origin
       - hire_date: Hire date
       - salary: Salary

    7. Feeding:
       - feedingID: Unique identifier for feeding record
       - animalID: Relationship to Animals table
       - foodTypeID: Relationship to FoodTypes table
       - staffID: Relationship to Staff table
       - feeding_date: Feeding date
       - quantity: Amount of food
       - notes: Notes

    8. AnimalCare:
       - careID: Unique identifier for care record
       - animalID: Relationship to Animals table
       - staffID: Relationship to Staff table
       - care_date: Care date
       - care_type: Type of care
       - notes: Notes

    AVAILABLE CLASSES AND METHODS:
    ----------------------------

    1. Species:
       - create(name, habitat, diet) -> Creates a new species record
       - read(species_id) -> Returns information about a specific species
       - read_all() -> Returns a list of all species
       - update(species_id, name, habitat, diet) -> Updates species information
       - delete(species_id) -> Removes a species record

    2. Animals:
       - create(name, species_id, gender=None, birthdate=None, health_status="Good") -> Creates a new animal record
       - read(animal_id) -> Returns information about a specific animal
       - read_all() -> Returns a list of all animals
       - update(animal_id, name, species_id, gender=None, birthdate=None, health_status=None) -> Updates animal information
       - delete(animal_id) -> Removes an animal record

    3. FoodTypes:
       - create(name, unit, storage_requirements=None) -> Creates a new food type record
       - read(food_type_id) -> Returns information about a specific food type
       - read_all() -> Returns a list of all food types
       - update(food_type_id, name, unit, storage_requirements=None) -> Updates food type information
       - delete(food_type_id) -> Removes a food type record

    4. FoodInventory:
       - create(food_type_id, quantity, expiration_date=None) -> Creates a new food inventory record
       - read(inventory_id) -> Returns information about a specific inventory
       - read_all() -> Returns a list of all inventory records
       - update_stock(inventory_id, quantity, expiration_date=None) -> Updates inventory information
       - delete(inventory_id) -> Removes an inventory record

    5. Roles:
       - create(title, department, description=None) -> Creates a new role record
       - read(role_id) -> Returns information about a specific role
       - read_all() -> Returns a list of all roles
       - update(role_id, title, department, description=None) -> Updates role information
       - delete(role_id) -> Removes a role record

    6. Staff:
       - create(first_name, last_name, role_id, country, salary, hire_date=None) -> Creates a new staff record
       - read(staff_id) -> Returns information about a specific staff member
       - read_all() -> Returns a list of all staff members
       - update(staff_id, first_name, last_name, role_id, country, salary, hire_date=None) -> Updates staff information
       - delete(staff_id) -> Removes a staff record

    7. Feeding:
       - create(animal_id, food_type_id, staff_id, quantity, notes=None, feeding_date=None) -> Creates a new feeding record
       - read(feeding_id) -> Returns information about a specific feeding
       - read_all() -> Returns a list of all feedings
       - update(feeding_id, animal_id, food_type_id, staff_id, quantity, notes=None, feeding_date=None) -> Updates feeding information
       - delete(feeding_id) -> Removes a feeding record

    USAGE EXAMPLES:
    -------------

    # Initialize the database
    from init_database import initialize_database
    initialize_database()

    # Add a new species
    tiger_id = Species.create("Tiger", "Asian Forests", "Carnivore")

    # Add a new animal
    simba_id = Animals.create("Simba", tiger_id, "Male")

    # Get information about an animal
    simba_info = Animals.read(simba_id)
    print(f"Name: {simba_info[1]}, Species: {simba_info[6]}")

    # Add a food type
    meat_id = FoodTypes.create("Meat", "kg", "Refrigerator")

    # Add food inventory
    inventory_id = FoodInventory.create(meat_id, 100.5, "2025-04-30")

    # Add a role
    keeper_id = Roles.create("Zookeeper", "Animal Care", "Responsible for animal care")

    # Add a staff member
    john_id = Staff.create("John", "Smith", keeper_id, "USA", 50000)

    # Record a feeding
    Feeding.create(simba_id, meat_id, john_id, 5.5, "Good appetite")

    # Get a list of all animals
    all_animals = Animals.read_all()
    for animal in all_animals:
        print(f"ID: {animal[0]}, Name: {animal[1]}, Species: {animal[6]}")

    # Update animal information
    Animals.update(simba_id, "King Simba", tiger_id, "Male")

    # Delete a record
    Animals.delete(simba_id)
    """

    print(help_text)
    return help_text


if __name__ == "__main__":
    help()