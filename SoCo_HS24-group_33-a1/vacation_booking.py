
def calculate_cost_BeachResort(thing) -> int:
    cost = thing["cost_per_day"]
    duration = thing["duration"]
    service = thing["surfing"]

    if service:
        return cost * duration + 100
    elif not service:
        return cost * duration
    else:
        return Exception("Service is not available")

def describe_package_BeachResort(thing) ->str:
    destination = thing["destination"]
    duration = thing["duration"]
    service = thing["surfing"]

    if service:
        return f"The {duration} long Beach Resort vacation in {destination} includes surfing."
    else:
        return f"The {duration} long Beach Resort vacation in {destination} does not include surfing."

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
