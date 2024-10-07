
BeachResort = {
    "_classname": "BeachResort",
    "_parent": VacationPackage,
    "cost": calculate_cost,
    "package": describe_package
}

def beach_resort_new(destination, cost_per_day, duration, surfing) -> dict:
    new_vacation = {
        "destination": destination,
        "cost_per_day": cost_per_day,
        "duration": duration,
        "surfing": surfing,
        "_class": BeachResort
    }
    return new_vacation
