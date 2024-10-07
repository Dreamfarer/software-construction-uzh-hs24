VacationPackage = {
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