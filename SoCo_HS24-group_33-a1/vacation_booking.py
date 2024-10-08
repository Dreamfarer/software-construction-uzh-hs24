# Abstract Method
def calculate_cost():
    raise NotImplementedError("This method must be implemented in subclass")


def calculate_cost_adventure(object: dict):
    days = object["duration_in_days"]
    cost = object["cost_per_day"]
    difficulty = object["difficulty_level"]

    if difficulty == "easy":
        return days * cost

    elif difficulty == "hard":
        return days * cost * 2

    else:
        return Exception("Undefined difficulty level")


def calculate_cost_BeachResort(object: dict) -> int:
    cost = object["cost_per_day"]
    duration = object["duration"]
    include_surfing = object["include_surfing"]

    if include_surfing:
        return cost * duration + 100
    elif not include_surfing:
        return cost * duration
    else:
        return Exception("Include_surfing is not available")


def calculate_cost_luxury_cruise(object: dict) -> int:
    cost = object["cost_per_day"]
    duration = object["duration"]
    if object["has_private_suite"]:
        return cost * duration * 1.5
    return cost * duration


# Abstract Method
def describe_package():
    raise NotImplementedError("This method must be implemented in subclass")


def describe_package_adventure(object: dict):
    destination = object["destination"]
    days = object["duration_in_days"]
    difficulty = object["difficulty_level"]

    return f"The {days} day long Adventure trip in {destination} is considered {difficulty}."


def describe_package_BeachResort(object: dict) -> str:
    destination = object["destination"]
    duration = object["duration"]
    include_surfing = object["include_surfing"]

    if include_surfing:
        return f"The {duration} long Beach Resort vacation in {destination} includes include_surfing."
    else:
        return f"The {duration} long Beach Resort vacation in {destination} does not include include_surfing."


def describe_package_luxury_cruise(object: dict) -> str:
    duration = object["duration_in_days"]
    destination = object["destination"]
    not_str = "" if object["has_private_suite"] else "not "
    return f"The {duration} day long Luxury Cruise in {destination} does {not_str}have a private suite."


VacationPackage = {
    "calculate_cost": calculate_cost,
    "describe_package": describe_package,
    "_classname": "VacationPackage",
    "_parent": None,
}

AdventureTrip = {
    "calculate_cost": calculate_cost_adventure,
    "describe_package": describe_package_adventure,
    "_classname": "AdventureTrip",
    "_parent": VacationPackage,
}

BeachResort = {
    "_classname": "BeachResort",
    "_parent": VacationPackage,
    "cost": calculate_cost_BeachResort,
    "package": describe_package_BeachResort,
}

LuxuryCruise = {
    "_classname": "LuxuryCruise",
    "_parent": VacationPackage,
    "cost": calculate_cost_luxury_cruise,
    "package": describe_package_luxury_cruise,
}


def vacation_package_new(destination: str, cost_per_day: int, duration_in_days: int):
    new_object = {
        "destination": destination,
        "cost_per_day": cost_per_day,
        "duration_in_days": duration_in_days,
        "_class": VacationPackage,
    }
    return new_object


def adventure_trip_new(
    destination: str, cost_per_day: int, duration_in_days: int, difficulty_level: str
):
    new_object = {
        "destination": destination,
        "cost_per_day": cost_per_day,
        "duration_in_days": duration_in_days,
        "difficulty_level": difficulty_level,
        "_class": AdventureTrip,
    }
    return new_object


def beach_resort_new(
    destination: str, cost_per_day: int, duration: int, include_surfing: bool
) -> dict:
    new_vacation = {
        "destination": destination,
        "cost_per_day": cost_per_day,
        "duration": duration,
        "include_surfing": include_surfing,
        "_class": BeachResort,
    }
    return new_vacation


def luxury_cruise_new(
    destination: str, cost_per_day: int, duration_in_days: int, has_private_suite: bool
):
    new_object = {
        "destination": destination,
        "cost_per_day": cost_per_day,
        "duration_in_days": duration_in_days,
        "has_private_suite": has_private_suite,
        "_class": LuxuryCruise,
    }
    return new_object
