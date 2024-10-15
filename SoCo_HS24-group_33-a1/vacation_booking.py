from collections.abc import Callable


def calculate_cost_adventure(cls: dict):
    days = cls["duration_in_days"]
    cost = cls["cost_per_day"]
    difficulty = cls["difficulty_level"]
    if difficulty == "easy":
        return days * cost
    elif difficulty == "hard":
        return days * cost * 2
    else:
        return Exception("Undefined difficulty level")


def calculate_cost_beach_resort(cls: dict) -> int:
    cost = cls["cost_per_day"]
    duration = cls["duration_in_days"]
    include_surfing = cls["include_surfing"]
    if include_surfing:
        return cost * duration + 100
    elif not include_surfing:
        return cost * duration
    else:
        return Exception("Include_surfing is not available")


def calculate_cost_luxury_cruise(cls: dict) -> int:
    cost = cls["cost_per_day"]
    duration = cls["duration_in_days"]
    if cls["has_private_suite"]:
        return cost * duration * 1.5
    return cost * duration


def describe_package_adventure(cls: dict):
    destination = cls["destination"]
    days = cls["duration_in_days"]
    difficulty = cls["difficulty_level"]
    return f"The {days} day long Adventure trip in {destination} is considered {difficulty}."


def describe_package_beach_resort(cls: dict) -> str:
    destination = cls["destination"]
    duration = cls["duration_in_days"]
    include_surfing = cls["include_surfing"]
    if include_surfing:
        return f"The {duration} long Beach Resort vacation in {destination} includes surfing."
    return f"The {duration} long Beach Resort vacation in {destination} does not include surfing."


def describe_package_luxury_cruise(cls: dict) -> str:
    duration = cls["duration_in_days"]
    destination = cls["destination"]
    not_str = "" if cls["has_private_suite"] else "not "
    return f"The {duration} day long Luxury Cruise in {destination} does {not_str}include a private suite."


Class = {"_parent": None}

VacationPackage = {
    "_parent": Class,
    "calculate_cost": None,
    "describe_package": None,
    "destination": None,
    "cost_per_day": None,
    "duration_in_days": None,
}

AdventureTrip = {
    "_parent": VacationPackage,
    "calculate_cost": calculate_cost_adventure,
    "describe_package": describe_package_adventure,
    "difficulty_level": None,
}

BeachResort = {
    "_parent": VacationPackage,
    "calculate_cost": calculate_cost_beach_resort,
    "describe_package": describe_package_beach_resort,
    "include_surfing": None,
}

LuxuryCruise = {
    "_parent": VacationPackage,
    "calculate_cost": calculate_cost_luxury_cruise,
    "describe_package": describe_package_luxury_cruise,
    "has_private_suite": None,
}


def merge_rec(cls: dict) -> dict:
    result = {}
    if "_parent" in cls and cls["_parent"] is not None:
        result.update(merge_rec(cls["_parent"]))
    result.update(cls)
    del result["_parent"]
    return result


def new(cls: dict, **kwargs) -> dict:
    merged_cls = merge_rec(cls)
    for key, value in merged_cls.items():
        if value is None:
            try:
                merged_cls[key] = kwargs[key]
            except:
                raise KeyError(f"{key} must be provided")
    return merged_cls


def find(cls: dict, method_name: str) -> Callable:
    try:
        return cls[method_name]
    except:
        raise NotImplementedError(f"Method '{method_name}' not found")


def call(cls: dict, method_name: str, *args):
    method = find(cls, method_name)
    return method(cls, *args)


if __name__ == "__main__":
    beach_resort = new(
        BeachResort,
        destination="Maldives",
        cost_per_day=100,
        duration_in_days=7,
        include_surfing=True,
    )
    adventure_trip = new(
        AdventureTrip,
        destination="Macchu Picchu",
        cost_per_day=150,
        duration_in_days=4,
        difficulty_level="easy",
    )
    luxury_cruise = new(
        LuxuryCruise,
        destination="Mediterranean",
        cost_per_day=100,
        duration_in_days=14,
        has_private_suite=False,
    )
    print(call(beach_resort, "calculate_cost"))
    print(call(adventure_trip, "calculate_cost"))
    print(call(luxury_cruise, "calculate_cost"))
    print(call(beach_resort, "describe_package"))
    print(call(adventure_trip, "describe_package"))
    print(call(luxury_cruise, "describe_package"))
