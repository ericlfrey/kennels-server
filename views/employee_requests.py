import sqlite3
import json
from models import Employee, Location
from .animal_requests import get_animals_by_location

EMPLOYEES = [
    {
        "id": 1,
        "name": "Jenna Solis"
    }
]


def get_all_employees():
    """gets all the employees"""

    with sqlite3.connect("./kennel.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id,
            l.name location_name,
            l.address location_address
        FROM employee e
        JOIN Location l
            ON l.id = e.location_id
        """)

        employees = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            employee = Employee(row['id'], row['name'],
                                row['address'], row['location_id'])

            location = Location(
                row['location_id'], row['location_name'], row['location_address'])

            employee.location = location.__dict__

            employees.append(employee.__dict__)

    return employees


# Function with a single parameter
def get_single_employee(id):
    """gets a single employee"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id,
            l.name location_name,
            l.address location_address
        FROM employee e
        JOIN Location l
            ON l.id = e.location_id
        WHERE e.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        employee = Employee(
            data['id'],
            data['name'],
            data['address'],
            data['location_id']
        )
        location = Location(
            data['location_id'],
            data['location_name'],
            data['location_address']
        )
        animals = get_animals_by_location(data['location_id'])
        employee.location = location.__dict__
        employee.animals = animals

        return employee.__dict__


def get_employees_by_location(location_id):
    """gets employees by their location ID"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            e.id,
            e.name,
            e.address,
            e.location_id
        from Employee e
        WHERE e.location_id = ?
        """, (location_id, ))

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(row['id'], row['name'],
                                row['address'], row['location_id'])
            employees.append(employee.__dict__)

    return employees


def create_employee(employee):
    """Creates a new employee"""
    max_id = EMPLOYEES[-1]["id"]

    new_id = max_id + 1

    employee["id"] = new_id

    EMPLOYEES.append(employee)

    return employee


def delete_employee(id):
    """Deletes single employee"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM employee
        WHERE id = ?
        """, (id, ))


def update_employee(id, new_employee):
    """Updates employee with Replacement"""
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            EMPLOYEES[index] = new_employee
            break
