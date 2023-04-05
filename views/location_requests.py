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
    return LOCATIONS


# Function with a single parameter
def get_single_location(id):
    """gets a single location"""
    requested_location = None

    for location in LOCATIONS:

        if location["id"] == id:
            requested_location = location

    return requested_location
