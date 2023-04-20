import sqlite3
# import json
from models import Animal, Location, Customer


def get_all_animals(query_params):
    """gets all the animals"""
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        sort_by = ""
        where_clause = ""

        if len(query_params) != 0:
            param = query_params[0]
            [qs_key, qs_value] = param.split("=")

            if qs_key == "_sortBy":
                if qs_value == 'location':
                    sort_by = " ORDER BY location_id"
                elif qs_value == 'customer':
                    sort_by = " ORDER BY customer_id"

            if qs_key == "location_id":
                where_clause = f"WHERE a.location_id = {qs_value}"

        sql_to_execute = f"""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.customer_id,
            a.location_id,
            l.name location_name,
            l.address location_address,
            c.name customer_name,
            c.address customer_address,
            c.email customer_email,
            c.password customer_password
        FROM Animal a
        JOIN Location l
            ON l.id = a.location_id
        JOIN Customer c
            ON c.id = a.customer_id
        {sort_by}
        {where_clause}
        """

        # Write the SQL query to get the information you want
        db_cursor.execute(sql_to_execute)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row
            animal = Animal(
                row['id'],
                row['name'],
                row['breed'],
                row['status'],
                row['customer_id'],
                row['location_id']
            )

            # Create a Location instance from the current row
            location = Location(
                row['location_id'],
                row['location_name'],
                row['location_address']
            )
            # Create a Customer instance from the current row
            customer = Customer(
                row['customer_id'],
                row['customer_name'],
                row['customer_address'],
                row['customer_email'],
                row['customer_password']
            )

            # Add the dictionary representation of the location to the animal
            animal.location = location.__dict__
            # Add the dictionary representation of the customer to the animal
            animal.customer = customer.__dict__

            # Add the dictionary representation of the animal to the list
            animals.append(animal.__dict__)
            # animals.append(customer.__dict__)

    return animals


# Function with a single parameter
def get_single_animal(id):
    """gets a single animal"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.customer_id,
            a.location_id,
            l.name location_name,
            l.address location_address,
            c.name customer_name,
            c.address customer_address,
            c.email customer_email,
            c.password customer_password
        FROM Animal a
        JOIN Location l
            ON l.id = a.location_id
        JOIN Customer c
            ON c.id = a.customer_id
        WHERE a.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(
            data['id'],
            data['name'],
            data['breed'],
            data['status'],
            data['customer_id'],
            data['location_id']
        )
        location = Location(
            data['location_id'],
            data['location_name'],
            data['location_address']
        )

        customer = Customer(
            data['customer_id'],
            data['customer_name'],
            data['customer_address'],
            data['customer_email'],
            data['customer_password']
        )

        animal.location = location.__dict__
        animal.customer = customer.__dict__

        return animal.__dict__


def get_animals_by_location(location_id):
    """gets animals by their location ID"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            a.id,
            a.name,
            a.breed,
            a.status,
            a.customer_id,
            a.location_id
        from Animal a
        WHERE a.location_id = ?
        """, (location_id, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(
                row['id'],
                row['name'],
                row['breed'],
                row['status'],
                row['customer_id'],
                row['location_id']
            )
            animals.append(animal.__dict__)

    return animals


def get_animals_by_search_term(search_term):
    """gets animals by their location ID"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            a.id,
            a.name,
            a.breed,
            a.status,
            a.customer_id,
            a.location_id
        from Animal a
        WHERE a.name LIKE ?
        """, (f"%{search_term}%", ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(
                row['id'],
                row['name'],
                row['breed'],
                row['status'],
                row['customer_id'],
                row['location_id']
            )
            animals.append(animal.__dict__)

    return animals


def get_animals_by_status(status):
    """gets animals by their status"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            a.id,
            a.name,
            a.breed,
            a.status,
            a.customer_id,
            a.location_id
        from Animal a
        WHERE a.status = ?
        """, (status, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(
                row['id'],
                row['name'],
                row['breed'],
                row['status'],
                row['customer_id'],
                row['location_id']
            )
            animals.append(animal.__dict__)

    return animals


def create_animal(new_animal):
    """Creates a new animal"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Animal
            ( name, breed, status, customer_id, location_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (
            new_animal['name'],
            new_animal['breed'],
            new_animal['status'],
            new_animal['customer_id'],
            new_animal['location_id'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_animal['id'] = id

    return new_animal


def delete_animal(id):
    """Deletes single animal"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))


def update_animal(id, new_animal):
    """Updates Animal with Replacement"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                breed = ?,
                status = ?,
                customer_id = ?,
                location_id = ?
        WHERE id = ?
        """, (
            new_animal['name'],
            new_animal['breed'],
            new_animal['status'],
            new_animal['customer_id'],
            new_animal['location_id'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
