import sqlite3
# import json
from models import Location
from .employee_requests import get_employees_by_location
from .animal_requests import get_animals_by_location

LOCATIONS = [
    {
        "id": 1,
        "name": "Nashville North",
        "address": "8422 Johnson Pike"
    },
    {
        "id": 2,
        "name": "Nashville South",
        "address": "209 Emory Drive"
    }
]


def get_all_locations():
    """gets all the locations"""
    with sqlite3.connect("./kennel.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address,
            COUNT(*) AS animals
        FROM Animal a
        JOIN Location l
            ON l.id = a.location_id
        GROUP BY l.id
        """)

        locations = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            location = Location(row['id'], row['name'],
                                row['address'], row['animals'])

            locations.append(location.__dict__)

    return locations


# Function with a single parameter
def get_single_location(id):
    """gets a single location"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address
        FROM location l
        WHERE l.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        location = Location(data['id'], data['name'],
                            data['address'], '')

        employees = get_employees_by_location(id)
        animals = get_animals_by_location(id)

        location.employees = employees
        location.animals = animals

        return location.__dict__


def create_location(location):
    """Creates a new location"""
    max_id = LOCATIONS[-1]["id"]

    new_id = max_id + 1

    location["id"] = new_id

    LOCATIONS.append(location)

    return location


def delete_location(id):
    """Deletes single location"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM location
        WHERE id = ?
        """, (id, ))


def update_location(id, new_location):
    """Updates location with Replacement"""
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            LOCATIONS[index] = new_location
            break
