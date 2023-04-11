DATABASE = {
    "animals": [
        {
            "id": 1,
            "name": "Snickers",
            "species": "Dog",
            "locationId": 1,
            "customerId": 1,
            "status": "Admitted"
        },
        {
            "id": 2,
            "name": "Roman",
            "species": "Dog",
            "locationId": 1,
            "customerId": 2,
            "status": "Admitted"
        },
        {
            "id": 3,
            "name": "Blue",
            "species": "Cat",
            "locationId": 2,
            "customerId": 1,
            "status": "Admitted"
        }
    ],
    "locations": [
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
    ],
    "customers": [
        {
            "id": 1,
            "name": "Ryan Tanay"
        }
    ],
    "employees": [
        {
            "id": 1,
            "name": "Jenna Solis"
        }
    ]
}


def get_all(db_key):
    """For GET requests to collection"""
    return DATABASE[db_key]


def retrieve(db_key, id):
    """For GET requests to a single resource"""
    requested_dict = None

    for dict in DATABASE[db_key]:

        if dict["id"] == id:
            requested_dict = dict

    return requested_dict


def create(new_dict, db_key):
    """For POST requests to a collection"""
    max_id = DATABASE[db_key][-1]["id"]

    new_id = max_id + 1

    new_dict["id"] = new_id

    DATABASE[db_key].append(new_dict)

    return new_dict


def update(id, new_dict, db_key):
    """For PUT requests to a single resource"""
    for index, dict in enumerate(DATABASE[db_key]):
        if dict["id"] == id:
            DATABASE[db_key][index] = new_dict
            break


def delete(db_key, id):
    """For DELETE requests to a single resource"""
    key_index = -1

    for index, dict in enumerate(DATABASE[db_key]):
        if dict["id"] == id:
            key_index = index

    if key_index >= 0:
        DATABASE[db_key].pop(key_index)
