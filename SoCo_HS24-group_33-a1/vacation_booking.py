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

def describe_package_adventure(object: dict):
    destination = object["destination"]
    days = object["duration_in_days"]
    difficulty = object["difficulty_level"]

    return f"The {days} day long Adventure trip in {destination} is considered {difficulty}."

AdventureTrip = {
    "calculate_cost": calculate_cost_adventure,
    "describe_package": describe_package_adventure,
    "_classname": "AdventureTrip",
    "_parent": VacationPackage 
}

def adventure_trip_new(destination: str, cost_per_day: int, duration_in_days: int, difficulty_level: str):
    new_object = {
        "destination": destination,
        "cost_per_day": cost_per_day,
        "duration_in_days": duration_in_days,
        "difficulty_level": difficulty_level,
        "_class": AdventureTrip
    }
    return new_object