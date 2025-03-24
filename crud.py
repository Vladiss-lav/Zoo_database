"""
CRUD (Create, Read, Update, Delete) operations for the Zoo Management System.

This module provides classes for interacting with the zoo database,
allowing management of animals, food inventory, and staff records.
"""
import sqlite3
import datetime

# Database name
DB_NAME = "zoo.db"


def get_connection():
    """
    Get a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A connection to the database
    """
    return sqlite3.connect(DB_NAME)


def transaction(func):
    """
    Decorator to handle database transactions.
    Commits if successful, rolls back on error.

    Args:
        func: The function to wrap with transaction handling

    Returns:
        wrapper: The wrapped function with transaction support
    """

    def wrapper(*args, **kwargs):
        connection = None
        try:
            # Get connection and pass it to the function
            connection = get_connection()
            # Replace the first arg (self) with connection if the function has args
            if args and hasattr(args[0], '__call__'):
                result = func(connection, *args[1:], **kwargs)
            else:
                result = func(connection, *args, **kwargs)
            # Commit if everything went well
            connection.commit()
            return result
        except Exception as e:
            # Roll back on error
            if connection:
                connection.rollback()
            print(f"Transaction error: {e}")
            raise
        finally:
            # Always close the connection
            if connection:
                connection.close()

    return wrapper


class Species:
    """Class for managing species records in the database"""

    @staticmethod
    @transaction
    def create(conn, name, habitat, diet):
        """
        Create a new species record.

        Args:
            conn (sqlite3.Connection): Database connection
            name (str): Species name
            habitat (str): Natural habitat
            diet (str): Diet type (e.g., Carnivore, Herbivore)

        Returns:
            int: ID of the newly created species
        """
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Species (name, habitat, diet) VALUES (?, ?, ?)",
            (name, habitat, diet)
        )
        return cursor.lastrowid

    @staticmethod
    @transaction
    def read(conn, species_id):
        """
        Read a species record by ID.

        Args:
            conn (sqlite3.Connection): Database connection
            species_id (int): Species ID to retrieve

        Returns:
            tuple: Species record or None if not found
        """
        cursor = conn.cursor()
        cursor.execute(
            "SELECT speciesID, name, habitat, diet FROM Species WHERE speciesID = ?",
            (species_id,)
        )
        return cursor.fetchone()

    @staticmethod
    @transaction
    def read_all(conn):
        """
        Read all species records.

        Args:
            conn (sqlite3.Connection): Database connection

        Returns:
            list: List of all species records
        """
        cursor = conn.cursor()
        cursor.execute("SELECT speciesID, name, habitat, diet FROM Species")
        return cursor.fetchall()

    @staticmethod
    @transaction
    def update(conn, species_id, name, habitat, diet):
        """
        Update a species record.

        Args:
            conn (sqlite3.Connection): Database connection
            species_id (int): Species ID to update
            name (str): Updated species name
            habitat (str): Updated habitat
            diet (str): Updated diet

        Returns:
            bool: True if update was successful, False otherwise
        """
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Species SET name = ?, habitat = ?, diet = ? WHERE speciesID = ?",
            (name, habitat, diet, species_id)
        )
        return cursor.rowcount > 0

    @staticmethod
    @transaction
    def delete(conn, species_id):
        """
        Delete a species record.

        Args:
            conn (sqlite3.Connection): Database connection
            species_id (int): Species ID to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Species WHERE speciesID = ?", (species_id,))
        return cursor.rowcount > 0


class Animals:
    """Class for managing animal records in the database"""

    @staticmethod
    @transaction
    def create(conn, name, species_id, gender=None, birthdate=None, health_status="Good"):
        """
        Create a new animal record.

        Args:
            conn (sqlite3.Connection): Database connection
            name (str): Animal name
            species_id (int): Species ID (foreign key to Species table)
            gender (str, optional): Animal gender ('Male', 'Female', or None)
            birthdate (str, optional): Birthdate in ISO format (YYYY-MM-DD)
            health_status (str, optional): Health status, defaults to 'Good'

        Returns:
            int: ID of the newly created animal
        """
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO Animals (name, speciesID, gender, birthdate, health_status) 
               VALUES (?, ?, ?, ?, ?)""",
            (name, species_id, gender, birthdate, health_status)
        )
        return cursor.lastrowid

    @staticmethod
    @transaction
    def read(conn, animal_id):
        """
        Read an animal record by ID.

        Args:
            conn (sqlite3.Connection): Database connection
            animal_id (int): Animal ID to retrieve

        Returns:
            tuple: Animal record or None if not found
        """
        cursor = conn.cursor()
        cursor.execute(
            """SELECT a.animalID, a.name, a.speciesID, a.gender, a.birthdate, a.health_status, s.name as species_name
               FROM Animals a
               JOIN Species s ON a.speciesID = s.speciesID
               WHERE a.animalID = ?""",
            (animal_id,)
        )
        return cursor.fetchone()

    @staticmethod
    @transaction
    def read_all(conn):
        """
        Read all animal records.

        Args:
            conn (sqlite3.Connection): Database connection

        Returns:
            list: List of all animal records
        """
        cursor = conn.cursor()
        cursor.execute(
            """SELECT a.animalID, a.name, a.speciesID, a.gender, a.birthdate, a.health_status, s.name as species_name
               FROM Animals a
               JOIN Species s ON a.speciesID = s.speciesID"""
        )
        return cursor.fetchall()

    @staticmethod
    @transaction
    def update(conn, animal_id, name, species_id, gender=None, birthdate=None, health_status=None):
        """
        Update an animal record.

        Args:
            conn (sqlite3.Connection): Database connection
            animal_id (int): Animal ID to update
            name (str): Updated animal name
            species_id (int): Updated species ID
            gender (str, optional): Updated gender
            birthdate (str, optional): Updated birthdate
            health_status (str, optional): Updated health status

        Returns:
            bool: True if update was successful, False otherwise
        """
        cursor = conn.cursor()

        # Get current values for any parameters that weren't specified
        if gender is None or birthdate is None or health_status is None:
            cursor.execute(
                "SELECT gender, birthdate, health_status FROM Animals WHERE animalID = ?",
                (animal_id,)
            )
            current = cursor.fetchone()
            if current:
                if gender is None:
                    gender = current[0]
                if birthdate is None:
                    birthdate = current[1]
                if health_status is None:
                    health_status = current[2]

        cursor.execute(
            """UPDATE Animals 
               SET name = ?, speciesID = ?, gender = ?, birthdate = ?, health_status = ? 
               WHERE animalID = ?""",
            (name, species_id, gender, birthdate, health_status, animal_id)
        )
        return cursor.rowcount > 0

    @staticmethod
    @transaction
    def delete(conn, animal_id):
        """
        Delete an animal record.

        Args:
            conn (sqlite3.Connection): Database connection
            animal_id (int): Animal ID to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Animals WHERE animalID = ?", (animal_id,))
        return cursor.rowcount > 0


class FoodTypes:
    """Class for managing food type records in the database"""

    @staticmethod
    @transaction
    def create(conn, name, unit, storage_requirements=None):
        """
        Create a new food type record.

        Args:
            conn (sqlite3.Connection): Database connection
            name (str): Food type name
            unit (str): Unit of measurement (e.g., kg, liters)
            storage_requirements (str, optional): Storage requirements

        Returns:
            int: ID of the newly created food type
        """
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO FoodTypes (name, unit, storage_requirements) VALUES (?, ?, ?)",
            (name, unit, storage_requirements)
        )
        return cursor.lastrowid

    @staticmethod
    @transaction
    def read(conn, food_type_id):
        """
        Read a food type record by ID.

        Args:
            conn (sqlite3.Connection): Database connection
            food_type_id (int): Food type ID to retrieve

        Returns:
            tuple: Food type record or None if not found
        """
        cursor = conn.cursor()
        cursor.execute(
            "SELECT foodTypeID, name, unit, storage_requirements FROM FoodTypes WHERE foodTypeID = ?",
            (food_type_id,)
        )
        return cursor.fetchone()

    @staticmethod
    @transaction
    def read_all(conn):
        """
        Read all food type records.

        Args:
            conn (sqlite3.Connection): Database connection

        Returns:
            list: List of all food type records
        """
        cursor = conn.cursor()
        cursor.execute("SELECT foodTypeID, name, unit, storage_requirements FROM FoodTypes")
        return cursor.fetchall()

    @staticmethod
    @transaction
    def update(conn, food_type_id, name, unit, storage_requirements=None):
        """
        Update a food type record.

        Args:
            conn (sqlite3.Connection): Database connection
            food_type_id (int): Food type ID to update
            name (str): Updated food type name
            unit (str): Updated unit of measurement
            storage_requirements (str, optional): Updated storage requirements

        Returns:
            bool: True if update was successful, False otherwise
        """
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE FoodTypes SET name = ?, unit = ?, storage_requirements = ? WHERE foodTypeID = ?",
            (name, unit, storage_requirements, food_type_id)
        )
        return cursor.rowcount > 0

    @staticmethod
    @transaction
    def delete(conn, food_type_id):
        """
        Delete a food type record.

        Args:
            conn (sqlite3.Connection): Database connection
            food_type_id (int): Food type ID to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        cursor = conn.cursor()
        cursor.execute("DELETE FROM FoodTypes WHERE foodTypeID = ?", (food_type_id,))
        return cursor.rowcount > 0


class FoodInventory:
    """Class for managing food inventory records in the database"""

    @staticmethod
    @transaction
    def create(conn, food_type_id, quantity, expiration_date=None):
        """
        Create a new food inventory record.

        Args:
            conn (sqlite3.Connection): Database connection
            food_type_id (int): Food type ID (foreign key to FoodTypes table)
            quantity (float): Quantity of food
            expiration_date (str, optional): Expiration date in ISO format (YYYY-MM-DD)

        Returns:
            int: ID of the newly created inventory record
        """
        cursor = conn.cursor()
        last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            """INSERT INTO FoodInventory (foodTypeID, quantity, expiration_date, last_updated) 
               VALUES (?, ?, ?, ?)""",
            (food_type_id, quantity, expiration_date, last_updated)
        )
        return cursor.lastrowid

    @staticmethod
    @transaction
    def read(conn, inventory_id):
        """
        Read a food inventory record by ID.

        Args:
            conn (sqlite3.Connection): Database connection
            inventory_id (int): Inventory ID to retrieve

        Returns:
            tuple: Inventory record or None if not found
        """
        cursor = conn.cursor()
        cursor.execute(
            """SELECT i.inventoryID, i.foodTypeID, ft.name, i.quantity, i.expiration_date, i.last_updated
               FROM FoodInventory i
               JOIN FoodTypes ft ON i.foodTypeID = ft.foodTypeID
               WHERE i.inventoryID = ?""",
            (inventory_id,)
        )
        return cursor.fetchone()

    @staticmethod
    @transaction
    def read_all(conn):
        """
        Read all food inventory records.

        Args:
            conn (sqlite3.Connection): Database connection

        Returns:
            list: List of all inventory records
        """
        cursor = conn.cursor()
        cursor.execute(
            """SELECT i.inventoryID, i.foodTypeID, ft.name, i.quantity, i.expiration_date, i.last_updated
               FROM FoodInventory i
               JOIN FoodTypes ft ON i.foodTypeID = ft.foodTypeID"""
        )
        return cursor.fetchall()

    @staticmethod
    @transaction
    def update_stock(conn, inventory_id, quantity, expiration_date=None):
        """
        Update a food inventory record.

        Args:
            conn (sqlite3.Connection): Database connection
            inventory_id (int): Inventory ID to update
            quantity (float): Updated quantity
            expiration_date (str, optional): Updated expiration date

        Returns:
            bool: True if update was successful, False otherwise
        """
        cursor = conn.cursor()
        last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Get current expiration date if not provided
        if expiration_date is None:
            cursor.execute(
                "SELECT expiration_date FROM FoodInventory WHERE inventoryID = ?",
                (inventory_id,)
            )
            current = cursor.fetchone()
            if current:
                expiration_date = current[0]

        cursor.execute(
            """UPDATE FoodInventory 
               SET quantity = ?, expiration_date = ?, last_updated = ? 
               WHERE inventoryID = ?""",
            (quantity, expiration_date, last_updated, inventory_id)
        )
        return cursor.rowcount > 0

    @staticmethod
    @transaction
    def delete(conn, inventory_id):
        """
        Delete a food inventory record.

        Args:
            conn (sqlite3.Connection): Database connection
            inventory_id (int): Inventory ID to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        cursor = conn.cursor()
        cursor.execute("DELETE FROM FoodInventory WHERE inventoryID = ?", (inventory_id,))
        return cursor.rowcount > 0


class Roles:
    """Class for managing role records in the database"""

    @staticmethod
    @transaction
    def create(conn, title, department, description=None):
        """
        Create a new role record.

        Args:
            conn (sqlite3.Connection): Database connection
            title (str): Role title
            department (str): Department
            description (str, optional): Role description

        Returns:
            int: ID of the newly created role
        """
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Roles (title, department, description) VALUES (?, ?, ?)",
            (title, department, description)
        )
        return cursor.lastrowid

    @staticmethod
    @transaction
    def read(conn, role_id):
        """
        Read a role record by ID.

        Args:
            conn (sqlite3.Connection): Database connection
            role_id (int): Role ID to retrieve

        Returns:
            tuple: Role record or None if not found
        """
        cursor = conn.cursor()
        cursor.execute(
            "SELECT roleID, title, department, description FROM Roles WHERE roleID = ?",
            (role_id,)
        )
        return cursor.fetchone()

    @staticmethod
    @transaction
    def read_all(conn):
        """
        Read all role records.

        Args:
            conn (sqlite3.Connection): Database connection

        Returns:
            list: List of all role records
        """
        cursor = conn.cursor()
        cursor.execute("SELECT roleID, title, department, description FROM Roles")
        return cursor.fetchall()

    @staticmethod
    @transaction
    def update(conn, role_id, title, department, description=None):
        """
        Update a role record.

        Args:
            conn (sqlite3.Connection): Database connection
            role_id (int): Role ID to update
            title (str): Updated title
            department (str): Updated department
            description (str, optional): Updated description

        Returns:
            bool: True if update was successful, False otherwise
        """
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Roles SET title = ?, department = ?, description = ? WHERE roleID = ?",
            (title, department, description, role_id)
        )
        return cursor.rowcount > 0

    @staticmethod
    @transaction
    def delete(conn, role_id):
        """
        Delete a role record.

        Args:
            conn (sqlite3.Connection): Database connection
            role_id (int): Role ID to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Roles WHERE roleID = ?", (role_id,))
        return cursor.rowcount > 0


class Staff:
    """Class for managing staff records in the database"""

    @staticmethod
    @transaction
    def create(conn, first_name, last_name, role_id, country, salary, hire_date=None):
        """
        Create a new staff record.

        Args:
            conn (sqlite3.Connection): Database connection
            first_name (str): Staff first name
            last_name (str): Staff last name
            role_id (int): Role ID (foreign key to Roles table)
            country (str): Country of origin
            salary (float): Salary
            hire_date (str, optional): Hire date in ISO format (YYYY-MM-DD)

        Returns:
            int: ID of the newly created staff record
        """
        cursor = conn.cursor()

        # Use current date if hire_date not provided
        if hire_date is None:
            hire_date = datetime.datetime.now().strftime("%Y-%m-%d")

        cursor.execute(
            """INSERT INTO Staff (firstName, lastName, roleID, country, hire_date, salary) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (first_name, last_name, role_id, country, hire_date, salary)
        )
        return cursor.lastrowid

    @staticmethod
    @transaction
    def read(conn, staff_id):
        """
        Read a staff record by ID.

        Args:
            conn (sqlite3.Connection): Database connection
            staff_id (int): Staff ID to retrieve

        Returns:
            tuple: Staff record or None if not found
        """
        cursor = conn.cursor()
        cursor.execute(
            """SELECT s.staffID, s.firstName, s.lastName, s.roleID, r.title as role_title, 
                      s.country, s.hire_date, s.salary
               FROM Staff s
               JOIN Roles r ON s.roleID = r.roleID
               WHERE s.staffID = ?""",
            (staff_id,)
        )
        return cursor.fetchone()

    @staticmethod
    @transaction
    def read_all(conn):
        """
        Read all staff records.

        Args:
            conn (sqlite3.Connection): Database connection

        Returns:
            list: List of all staff records
        """
        cursor = conn.cursor()
        cursor.execute(
            """SELECT s.staffID, s.firstName, s.lastName, s.roleID, r.title as role_title, 
                      s.country, s.hire_date, s.salary
               FROM Staff s
               JOIN Roles r ON s.roleID = r.roleID"""
        )
        return cursor.fetchall()

    @staticmethod
    @transaction
    def update(conn, staff_id, first_name, last_name, role_id, country, salary, hire_date=None):
        """
        Update a staff record.

        Args:
            conn (sqlite3.Connection): Database connection
            staff_id (int): Staff ID to update
            first_name (str): Updated first name
            last_name (str): Updated last name
            role_id (int): Updated role ID
            country (str): Updated country
            salary (float): Updated salary
            hire_date (str, optional): Updated hire date

        Returns:
            bool: True if update was successful, False otherwise
        """
        cursor = conn.cursor()

        # Get current hire_date if not provided
        if hire_date is None:
            cursor.execute(
                "SELECT hire_date FROM Staff WHERE staffID = ?",
                (staff_id,)
            )
            current = cursor.fetchone()
            if current:
                hire_date = current[0]

        cursor.execute(
            """UPDATE Staff 
               SET firstName = ?, lastName = ?, roleID = ?, country = ?, hire_date = ?, salary = ? 
               WHERE staffID = ?""",
            (first_name, last_name, role_id, country, hire_date, salary, staff_id)
        )
        return cursor.rowcount > 0

    @staticmethod
    @transaction
    def delete(conn, staff_id):
        """
        Delete a staff record.

        Args:
            conn (sqlite3.Connection): Database connection
            staff_id (int): Staff ID to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Staff WHERE staffID = ?", (staff_id,))
        return cursor.rowcount > 0


class Feeding:
    """Class for managing feeding records in the database"""

    @staticmethod
    @transaction
    def create(conn, animal_id, food_type_id, staff_id, quantity, notes=None, feeding_date=None):
        """
        Create a new feeding record.

        Args:
            conn (sqlite3
        """