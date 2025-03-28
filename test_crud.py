import unittest
import sqlite3
import os
import datetime

# Import the module to test
from crud import (
    Species, Animals, FoodTypes, FoodInventory,
    Roles, Staff, Feeding, get_connection
)

class TestZooManagementSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up test database before running tests
        """
        # Use a separate test database
        cls.test_db_name = "test_zoo.db"
        os.environ['DB_NAME'] = cls.test_db_name

        # Create test database and tables
        cls._create_test_database()

    @classmethod
    def _create_test_database(cls):
        """
        Create test database with necessary tables
        """
        conn = sqlite3.connect(cls.test_db_name)
        cursor = conn.cursor()

        # Create Species table
        cursor.execute('''
        CREATE TABLE Species (
            speciesID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            habitat TEXT,
            diet TEXT
        )''')

        # Create Animals table
        cursor.execute('''
        CREATE TABLE Animals (
            animalID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            speciesID INTEGER,
            gender TEXT,
            birthdate TEXT,
            health_status TEXT,
            FOREIGN KEY(speciesID) REFERENCES Species(speciesID)
        )''')

        # Create FoodTypes table
        cursor.execute('''
        CREATE TABLE FoodTypes (
            foodTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            unit TEXT,
            storage_requirements TEXT
        )''')

        # Create FoodInventory table
        cursor.execute('''
        CREATE TABLE FoodInventory (
            inventoryID INTEGER PRIMARY KEY AUTOINCREMENT,
            foodTypeID INTEGER,
            quantity REAL,
            expiration_date TEXT,
            last_updated TEXT,
            FOREIGN KEY(foodTypeID) REFERENCES FoodTypes(foodTypeID)
        )''')

        # Create Roles table
        cursor.execute('''
        CREATE TABLE Roles (
            roleID INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            department TEXT,
            description TEXT
        )''')

        # Create Staff table
        cursor.execute('''
        CREATE TABLE Staff (
            staffID INTEGER PRIMARY KEY AUTOINCREMENT,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            roleID INTEGER,
            country TEXT,
            hire_date TEXT,
            salary REAL,
            FOREIGN KEY(roleID) REFERENCES Roles(roleID)
        )''')

        # Create Feeding table
        cursor.execute('''
        CREATE TABLE Feeding (
            feedingID INTEGER PRIMARY KEY AUTOINCREMENT,
            animalID INTEGER,
            foodTypeID INTEGER,
            staffID INTEGER,
            quantity REAL,
            notes TEXT,
            feeding_date TEXT,
            FOREIGN KEY(animalID) REFERENCES Animals(animalID),
            FOREIGN KEY(foodTypeID) REFERENCES FoodTypes(foodTypeID),
            FOREIGN KEY(staffID) REFERENCES Staff(staffID)
        )''')

        conn.commit()
        conn.close()

    @classmethod
    def tearDownClass(cls):
        """
        Clean up test database after tests
        """
        # Remove test database file
        if os.path.exists(cls.test_db_name):
            os.remove(cls.test_db_name)

    def setUp(self):
        """
        Reset the necessary tables before each test
        """
        conn = get_connection()
        cursor = conn.cursor()

        # Clear tables
        tables = ['Species', 'Animals', 'FoodTypes', 'FoodInventory', 'Roles', 'Staff', 'Feeding']
        for table in tables:
            cursor.execute(f'DELETE FROM {table}')

        conn.commit()
        conn.close()

    def test_species_crud(self):
        """
        Test CRUD operations for Species class
        """
        # Create
        species_id = Species.create("Lion", "Savanna", "Carnivore")
        self.assertIsNotNone(species_id)

        # Read
        species = Species.read(species_id)
        self.assertIsNotNone(species)
        self.assertEqual(species[1], "Lion")
        self.assertEqual(species[2], "Savanna")
        self.assertEqual(species[3], "Carnivore")

        # Update
        update_result = Species.update(species_id, "African Lion", "African Savanna", "Apex Predator")
        self.assertTrue(update_result)

        updated_species = Species.read(species_id)
        self.assertEqual(updated_species[1], "African Lion")
        self.assertEqual(updated_species[2], "African Savanna")
        self.assertEqual(updated_species[3], "Apex Predator")

        # Read All
        all_species = Species.read_all()
        self.assertEqual(len(all_species), 1)

        # Delete
        delete_result = Species.delete(species_id)
        self.assertTrue(delete_result)

        deleted_species = Species.read(species_id)
        self.assertIsNone(deleted_species)

    def test_animals_crud(self):
        """
        Test CRUD operations for Animals class
        """
        # First create a species
        species_id = Species.create("Tiger", "Jungle", "Carnivore")

        # Create
        animal_id = Animals.create("Simba", species_id, "Male", "2020-01-01", "Good")
        self.assertIsNotNone(animal_id)

        # Read
        animal = Animals.read(animal_id)
        self.assertIsNotNone(animal)
        self.assertEqual(animal[1], "Simba")
        self.assertEqual(animal[2], species_id)
        self.assertEqual(animal[3], "Male")

        # Update
        update_result = Animals.update(animal_id, "Simba Jr", species_id, "Male", "2020-01-02", "Excellent")
        self.assertTrue(update_result)

        updated_animal = Animals.read(animal_id)
        self.assertEqual(updated_animal[1], "Simba Jr")
        self.assertEqual(updated_animal[5], "Excellent")

        # Read All
        all_animals = Animals.read_all()
        self.assertEqual(len(all_animals), 1)

        # Delete
        delete_result = Animals.delete(animal_id)
        self.assertTrue(delete_result)

        deleted_animal = Animals.read(animal_id)
        self.assertIsNone(deleted_animal)

    def test_food_types_crud(self):
        """
        Test CRUD operations for FoodTypes class
        """
        # Create
        food_type_id = FoodTypes.create("Meat", "kg", "Refrigerated")
        self.assertIsNotNone(food_type_id)

        # Read
        food_type = FoodTypes.read(food_type_id)
        self.assertIsNotNone(food_type)
        self.assertEqual(food_type[1], "Meat")
        self.assertEqual(food_type[2], "kg")

        # Update
        update_result = FoodTypes.update(food_type_id, "Fresh Meat", "lbs", "Frozen")
        self.assertTrue(update_result)

        updated_food_type = FoodTypes.read(food_type_id)
        self.assertEqual(updated_food_type[1], "Fresh Meat")
        self.assertEqual(updated_food_type[2], "lbs")

        # Read All
        all_food_types = FoodTypes.read_all()
        self.assertEqual(len(all_food_types), 1)

        # Delete
        delete_result = FoodTypes.delete(food_type_id)
        self.assertTrue(delete_result)

        deleted_food_type = FoodTypes.read(food_type_id)
        self.assertIsNone(deleted_food_type)

    def test_roles_crud(self):
        """
        Test CRUD operations for Roles class
        """
        # Create
        role_id = Roles.create("Zookeeper", "Animal Care", "Responsible for animal feeding")
        self.assertIsNotNone(role_id)

        # Read
        role = Roles.read(role_id)
        self.assertIsNotNone(role)
        self.assertEqual(role[1], "Zookeeper")
        self.assertEqual(role[2], "Animal Care")

        # Update
        update_result = Roles.update(role_id, "Senior Zookeeper", "Animal Management", "Advanced animal care")
        self.assertTrue(update_result)

        updated_role = Roles.read(role_id)
        self.assertEqual(updated_role[1], "Senior Zookeeper")
        self.assertEqual(updated_role[2], "Animal Management")

        # Read All
        all_roles = Roles.read_all()
        self.assertEqual(len(all_roles), 1)

        # Delete
        delete_result = Roles.delete(role_id)
        self.assertTrue(delete_result)

        deleted_role = Roles.read(role_id)
        self.assertIsNone(deleted_role)

    def test_staff_crud(self):
        """
        Test CRUD operations for Staff class
        """
        # First create a role
        role_id = Roles.create("Zookeeper", "Animal Care")

        # Create
        staff_id = Staff.create("John", "Doe", role_id, "USA", 50000, "2023-01-01")
        self.assertIsNotNone(staff_id)

        # Read
        staff = Staff.read(staff_id)
        self.assertIsNotNone(staff)
        self.assertEqual(staff[1], "John")
        self.assertEqual(staff[2], "Doe")
        self.assertEqual(staff[4], "Zookeeper")

        # Update
        update_result = Staff.update(staff_id, "Jane", "Doe", role_id, "Canada", 55000, "2023-02-01")
        self.assertTrue(update_result)

        updated_staff = Staff.read(staff_id)
        self.assertEqual(updated_staff[1], "Jane")
        self.assertEqual(updated_staff[5], "Canada")

        # Read All
        all_staff = Staff.read_all()
        self.assertEqual(len(all_staff), 1)

        # Delete
        delete_result = Staff.delete(staff_id)
        self.assertTrue(delete_result)

        deleted_staff = Staff.read(staff_id)
        self.assertIsNone(deleted_staff)

    def test_feeding_crud(self):
        """
        Test CRUD operations for Feeding class
        """
        # Create dependencies first
        species_id = Species.create("Lion", "Savanna", "Carnivore")
        animal_id = Animals.create("Leo", species_id)
        food_type_id = FoodTypes.create("Meat", "kg")
        role_id = Roles.create("Zookeeper", "Animal Care")
        staff_id = Staff.create("John", "Doe", role_id, "USA", 50000)

        # Create
        feeding_id = Feeding.create(animal_id, food_type_id, staff_id, 5.5, "Morning feeding")
        self.assertIsNotNone(feeding_id)

        # Read
        feeding = Feeding.read(feeding_id)
        self.assertIsNotNone(feeding)
        self.assertEqual(feeding[1], animal_id)
        self.assertEqual(feeding[3], food_type_id)
        self.assertEqual(feeding[7], 5.5)

        # Update
        update_result = Feeding.update(feeding_id, animal_id, food_type_id, staff_id, 6.0, "Evening feeding")
        self.assertTrue(update_result)

        updated_feeding = Feeding.read(feeding_id)
        self.assertEqual(updated_feeding[7], 6.0)
        self.assertEqual(updated_feeding[8], "Evening feeding")

        # Read All
        all_feedings = Feeding.read_all()
        self.assertEqual(len(all_feedings), 1)

        # Delete
        delete_result = Feeding.delete(feeding_id)
        self.assertTrue(delete_result)

        deleted_feeding = Feeding.read(feeding_id)
        self.assertIsNone(deleted_feeding)

if __name__ == '__main__':
    unittest.main()