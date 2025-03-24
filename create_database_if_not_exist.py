"""
Module for initializing the zoo database with normalized tables.
This script creates the necessary tables for the Zoo Management System.
"""
import sqlite3
import os


def initialize_database(db_name="zoo.db", force_new=False):
    """
    Initialize the database with the required tables.

    Args:
        db_name (str): Name of the database file
        force_new (bool): If True, removes existing database before creating a new one

    Returns:
        bool: True if initialization was successful
    """
    # If force_new and file exists, remove it
    if force_new and os.path.exists(db_name):
        os.remove(db_name)

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create Species table (Lookup table for animal species)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Species (
        speciesID INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        habitat TEXT NOT NULL,
        diet TEXT NOT NULL
    )
    ''')

    # Create Animals table with relationship to Species
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Animals (
        animalID INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        speciesID INTEGER NOT NULL,
        gender TEXT CHECK(gender IN ('Male', 'Female', NULL)),
        birthdate TEXT,
        health_status TEXT DEFAULT 'Good',
        FOREIGN KEY (speciesID) REFERENCES Species(speciesID)
    )
    ''')

    # Create FoodTypes table (Lookup table for food types)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS FoodTypes (
        foodTypeID INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        unit TEXT NOT NULL,
        storage_requirements TEXT
    )
    ''')

    # Create FoodInventory table with relationship to FoodTypes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS FoodInventory (
        inventoryID INTEGER PRIMARY KEY,
        foodTypeID INTEGER NOT NULL,
        quantity REAL NOT NULL CHECK(quantity >= 0),
        expiration_date TEXT,
        last_updated TEXT NOT NULL,
        FOREIGN KEY (foodTypeID) REFERENCES FoodTypes(foodTypeID)
    )
    ''')

    # Create Roles table (Lookup table for staff roles)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Roles (
        roleID INTEGER PRIMARY KEY,
        title TEXT NOT NULL UNIQUE,
        department TEXT NOT NULL,
        description TEXT
    )
    ''')

    # Create Staff table with relationship to Roles
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Staff (
        staffID INTEGER PRIMARY KEY,
        firstName TEXT NOT NULL,
        lastName TEXT NOT NULL,
        roleID INTEGER NOT NULL,
        country TEXT NOT NULL,
        hire_date TEXT NOT NULL,
        salary REAL NOT NULL CHECK(salary > 0),
        FOREIGN KEY (roleID) REFERENCES Roles(roleID)
    )
    ''')

    # Create Feeding table for tracking which animals are fed which foods
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Feeding (
        feedingID INTEGER PRIMARY KEY,
        animalID INTEGER NOT NULL,
        foodTypeID INTEGER NOT NULL,
        staffID INTEGER NOT NULL,
        feeding_date TEXT NOT NULL,
        quantity REAL NOT NULL CHECK(quantity > 0),
        notes TEXT,
        FOREIGN KEY (animalID) REFERENCES Animals(animalID),
        FOREIGN KEY (foodTypeID) REFERENCES FoodTypes(foodTypeID),
        FOREIGN KEY (staffID) REFERENCES Staff(staffID)
    )
    ''')

    # Create AnimalCare table for tracking medical care, training, etc.
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS AnimalCare (
        careID INTEGER PRIMARY KEY,
        animalID INTEGER NOT NULL,
        staffID INTEGER NOT NULL,
        care_date TEXT NOT NULL,
        care_type TEXT NOT NULL,
        notes TEXT,
        FOREIGN KEY (animalID) REFERENCES Animals(animalID),
        FOREIGN KEY (staffID) REFERENCES Staff(staffID)
    )
    ''')

    # Insert some default data
    # Insert species
    species_data = [
        (1, 'Lion', 'Savanna', 'Carnivore'),
        (2, 'Elephant', 'Grassland', 'Herbivore'),
        (3, 'Penguin', 'Polar', 'Piscivore'),
        (4, 'Giraffe', 'Savanna', 'Herbivore')
    ]

    cursor.executemany("INSERT OR IGNORE INTO Species (speciesID, name, habitat, diet) VALUES (?, ?, ?, ?)",
                       species_data)

    # Insert food types
    food_data = [
        (1, 'Meat', 'kg', 'Refrigerated'),
        (2, 'Hay', 'kg', 'Dry storage'),
        (3, 'Fish', 'kg', 'Frozen'),
        (4, 'Fruits', 'kg', 'Fresh produce'),
        (5, 'Vegetables', 'kg', 'Fresh produce')
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO FoodTypes (foodTypeID, name, unit, storage_requirements) VALUES (?, ?, ?, ?)",
        food_data)

    # Insert roles
    roles_data = [
        (1, 'Zookeeper', 'Animal Care', 'Responsible for daily care of animals'),
        (2, 'Veterinarian', 'Medical', 'Provides medical care to animals'),
        (3, 'Manager', 'Administration', 'Oversees zoo operations'),
        (4, 'Guide', 'Education', 'Conducts tours and educational programs')
    ]

    cursor.executemany("INSERT OR IGNORE INTO Roles (roleID, title, department, description) VALUES (?, ?, ?, ?)",
                       roles_data)

    conn.commit()
    conn.close()

    return True


if __name__ == "__main__":
    # When run directly, initialize the database
    initialize_database(force_new=True)
    print("Database initialized successfully!")