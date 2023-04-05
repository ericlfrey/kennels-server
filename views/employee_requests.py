EMPLOYEES = [
    {
        "id": 1,
        "name": "Jenna Solis"
    }
]


def get_all_employees():
    """gets all the employees"""
    return EMPLOYEES


# Function with a single parameter
def get_single_employee(id):
    """gets a single employee"""
    requested_employee = None

    for employee in EMPLOYEES:

        if employee["id"] == id:
            requested_employee = employee

    return requested_employee
