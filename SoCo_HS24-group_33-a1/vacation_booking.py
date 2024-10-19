from collections.abc import Callable

booked_vacations = []  # Keep track of all instanciated vacations


def calculate_cost_adventure(cls: dict) -> int:
    days = cls["duration_in_days"]
    cost = cls["cost_per_day"]
    difficulty = cls["difficulty_level"]
    if difficulty == "easy":
        return days * cost
    return days * cost * 2


def calculate_cost_beach_resort(cls: dict) -> int:
    cost = cls["cost_per_day"]
    duration = cls["duration_in_days"]
    include_surfing = cls["include_surfing"]
    if duration == 0:
        return 0
    elif include_surfing:
        return cost * duration + 100
    return cost * duration


def calculate_cost_luxury_cruise(cls: dict) -> int:
    cost = cls["cost_per_day"]
    duration = cls["duration_in_days"]
    if cls["has_private_suite"]:
        return cost * duration * 1.5
    return cost * duration


def describe_package_adventure(cls: dict) -> str:
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


def calculate_total_cost(cls: dict) -> int:
    total_cost = 0
    for vacation in booked_vacations:
        if cls["search_term"].lower() in vacation["_name"].lower():
            total_cost += call(vacation, "calculate_cost")
    return total_cost


def extract_total_vacation_summary(cls: dict) -> str:
    vacation_summary = ""
    for vacation in booked_vacations:
        if cls["search_term"].lower() in vacation["_name"].lower():
            vacation_summary += call(vacation, "describe_package") + "\n"
    return vacation_summary[:-1]


Class = {"_parent": None, "_name": "Class", "_types": {}}

VacationPackage = {
    "_parent": Class,
    "_name": "VacationPackage",
    "calculate_cost": None,
    "describe_package": None,
    "destination": None,
    "cost_per_day": None,
    "duration_in_days": None,
}

AdventureTrip = {
    "_parent": VacationPackage,
    "_name": "AdventureTrip",
    "calculate_cost": calculate_cost_adventure,
    "describe_package": describe_package_adventure,
    "difficulty_level": None,
}

BeachResort = {
    "_parent": VacationPackage,
    "_name": "BeachResort",
    "calculate_cost": calculate_cost_beach_resort,
    "describe_package": describe_package_beach_resort,
    "include_surfing": None,
}

LuxuryCruise = {
    "_parent": VacationPackage,
    "_name": "LuxuryCruise",
    "calculate_cost": calculate_cost_luxury_cruise,
    "describe_package": describe_package_luxury_cruise,
    "has_private_suite": None,
}

VacationBookingSummary = {
    "_parent": Class,
    "_name": "VacationBookingSummary",
    "calculate_cost": calculate_total_cost,
    "describe_package": extract_total_vacation_summary,
    "search_term": None,
}


Type_Class = {"_parent": str, "_name": str, "_types": dict}

Type_VacationPackage = {
    "_parent": dict,
    "_name": str,
    "calculate_cost": Callable,
    "describe_package": Callable,
    "destination": str,
    "cost_per_day": lambda x: isinstance(x, int) and x >= 0,
    "duration_in_days": int,
}

Type_AdventureTrip = {
    "difficulty_level": ["easy", "hard"],
}

Type_BeachResort = {
    "include_surfing": bool,
}

Type_LuxuryCruise = {
    "has_private_suite": bool,
}

Type_VacationBookingSummary = {
    "_name": str,
    "calculate_cost": Callable,
    "describe_package": Callable,
    "search_term": str,
}


def find_tests() -> list[Callable]:
    """
    Find all callables starting with "Test_" in the global symbol table.

    Returns:
        list[Callable]: A list containing all the found callables.
    """
    tests = []
    for key in globals().items:
        if key.startswith("Test_"):
            tests.append(globals()[key])
    return tests


def find_symtable(cls_name: str) -> dict:
    """
    Retrieve a dictionary (object) starting with "Type_" from the global symbol table.

    Args:
        cls_name (str): The name of the class whose associated types to find.

    Returns:
        dict: The found dictionary (object).

    Raises:
        KeyError: If the class whose associated types to find is not found in the global symbol table.
    """
    type_name = "Type_" + cls_name
    try:
        return globals()[type_name]
    except:
        raise KeyError(f"Method '{type_name}' was not found")


def find_cls(cls: dict, method_name: str) -> Callable:
    """
    Find a method inside the dictionary (object) and return it.

    Args:
        cls (dict): The dictionary (object) in which to find the method.
        method_name (str): The name of the method to be found.

    Returns:
        Callable: The found method.

    Raises:
        KeyError: If the method is not found in the dictionary.
    """
    try:
        return cls[method_name]
    except:
        raise KeyError(f"Method '{method_name}' was not found")


def call(cls: dict, method_name: str, *args) -> any:
    """
    Execute the specified method on the given dictionary (object) and return its result.

    Args:
        cls (dict): The dictionary (object) on which to call the method.
        method_name (str): The name of the method to be called.
        *args: Additional arguments to pass to the method.

    Returns:
        Any: The return value of the executed method.
    """
    method = find_cls(cls, method_name)
    return method(cls, *args)


def merge_rec(cls: dict) -> dict:
    """
    Recursively merge the methods and attributes of a dictionary (class) with those of its parent.
    Additionally, update the '_types' key with type information from the symbol table based on the class name.

    Args:
        cls (dict): The dictionary (class) to be instantiated.
        symbol_table (Callable): A function that returns a symbol table dictionary ('globals', 'locals').

    Returns:
        dict: The newly instantiated dictionary (object) with merged attributes, methods and type information.
    """
    result = {}
    if "_parent" in cls and cls["_parent"] is not None:
        result.update(merge_rec(cls["_parent"]))
    result.update(cls)
    _type = find_symtable(result["_name"])
    result["_types"].update(_type)
    del result["_parent"]
    return result


def new(cls: dict, **kwargs) -> dict:
    """
    Instantiates a new dictionary containing all methods and attributes of the provided dictionary (class) and all its parents. Fills its attributes with the values provided via '**kwargs'.

    Args:
        cls (dict): The dictionary (class) to be instantiated.
        **kwargs: Attributes to set on the new instance. If 'symbol_table' is not provided, it defaults to 'globals'.

    Returns:
        dict: The newly instantiated dictionary filled with the provided attributes.

    Raises:
        KeyError: If a required attribute is not provided in '**kwargs'.
        TypeError: If an attribute does not match the expected type.
    """
    merged_cls = merge_rec(cls)
    if merged_cls["_name"] == "VacationBookingSummary":
        if not "search_term" in kwargs:
            merged_cls["search_term"] = ""

    for key, value in merged_cls.items():
        if value is None:
            if not key in kwargs:
                raise KeyError(f"{key} must be provided")
            if not key in merged_cls:
                raise KeyError(f"{key} does not exist on {merged_cls['_name']}")
            merged_cls[key] = kwargs[key]
            _type = merged_cls["_types"][key]
            if callable(_type):
                if not _type(kwargs[key]):
                    raise TypeError(f"{key} must be of {_type}")
            elif isinstance(_type, list):
                if not kwargs[key] in _type:
                    raise TypeError(f"{key} must be of {_type}")
            elif not isinstance(kwargs[key], _type):
                raise TypeError(f"{key} must be a {_type}")
    if not merged_cls["_name"] == "VacationBookingSummary":
        booked_vacations.append(merged_cls)
    return merged_cls


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

    vacation_booking_summary = new(VacationBookingSummary, search_term="Cruise")
    print(call(vacation_booking_summary, "calculate_cost"))
    print(call(vacation_booking_summary, "describe_package"))

    vacation_booking_summary = new(VacationBookingSummary, search_term="Beach")
    print(call(vacation_booking_summary, "calculate_cost"))
    print(call(vacation_booking_summary, "describe_package"))

    vacation_booking_summary = new(VacationBookingSummary, search_term="Adv")
    print(call(vacation_booking_summary, "calculate_cost"))
    print(call(vacation_booking_summary, "describe_package"))

    vacation_booking_summary = new(VacationBookingSummary)
    print(call(vacation_booking_summary, "calculate_cost"))
    print(call(vacation_booking_summary, "describe_package"))
