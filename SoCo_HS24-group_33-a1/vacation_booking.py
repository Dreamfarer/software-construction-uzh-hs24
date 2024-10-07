# Abstract Method
def calculate_cost():
    raise NotImplementedError("This method must be implemented in subclass")

# Abstract Method
def describe_package():
    raise NotImplementedError("This method must be implemented in subclass")

VacationPackage = {
    "calculate_cost": calculate_cost,
    "describe_package": describe_package,
    "_classname": "VacationPackage",
    "_parent": None
}

def vacation_package_new(destination: str, cost_per_day: int, duration_in_days: int):
    new_object = {
        "destination": destination,
        "cost_per_day": cost_per_day,
        "duration_in_days": duration_in_days,
        "_class": VacationPackage
    }
    return new_object