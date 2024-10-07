AdventureTrip = {
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