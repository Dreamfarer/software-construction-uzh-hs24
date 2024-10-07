
def calculate_cost_BeachResort(object: dict) -> int:
    cost = object["cost_per_day"]
    duration = object["duration"]
    include_surfing = object["surfing"]

    if include_surfing:
        return cost * duration + 100
    elif not include_surfing:
        return cost * duration
    else:
        return Exception("Surfing is not available")

def describe_package_BeachResort(object: dict) -> str:
    destination = object["destination"]
    duration = object["duration"]
    include_surfing = object["surfing"]

    if include_surfing:
        return f"The {duration} long Beach Resort vacation in {destination} includes surfing."
    else:
        return f"The {duration} long Beach Resort vacation in {destination} does not include surfing."

BeachResort = {
    "_classname": "BeachResort",
    "_parent": VacationPackage,
    "cost": calculate_cost_BeachResort,
    "package": describe_package_BeachResort
}

def beach_resort_new(destination: str, cost_per_day: int, duration: int, surfing: bool) -> dict:
    new_vacation = {
        "destination": destination,
        "cost_per_day": cost_per_day,
        "duration": duration,
        "include_surfing": surfing,
        "_class": BeachResort
    }
    return new_vacation
