CUSTOMERS = [
    {
        "id": 1,
        "name": "Ryan Tanay"
    }
]


def get_all_customers():
    """gets all the customers"""
    return CUSTOMERS


# Function with a single parameter
def get_single_customer(id):
    """gets a single customer"""
    requested_customer = None

    for customer in CUSTOMERS:

        if customer["id"] == id:
            requested_customer = customer

    return requested_customer


def create_customer(customer):
    """Creates a new customer"""
    max_id = CUSTOMERS[-1]["id"]

    new_id = max_id + 1

    customer["id"] = new_id

    CUSTOMERS.append(customer)

    return customer
