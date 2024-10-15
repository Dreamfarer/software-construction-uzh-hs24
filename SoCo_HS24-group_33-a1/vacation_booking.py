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

Type_Class = {"_parent": str, "_name": "str", "_types": dict}

Type_VacationPackage = {
    "_parent": dict,
    "_name": str,
    "calculate_cost": Callable,
    "describe_package": Callable,
    "destination": str,
    "cost_per_day": int,
    "duration_in_days": int,
}

Type_AdventureTrip = {
    "difficulty_level": str,
}

Type_BeachResort = {
    "include_surfing": bool,
}

Type_LuxuryCruise = {
    "has_private_suite": bool,
}


def find_tests(symbol_table: Callable) -> list[Callable]:
    """
    Find all callables starting with "Test_" in the provided symbol table.

    Args:
        symbol_table (Callable): A function that returns a symbol table dictionary ('globals', 'locals').

    Returns:
        list[Callable]: A list containing all the found callables.
    """
    tests = []
    for key in symbol_table().items:
        if key.startswith("Test_"):
            tests.append(symbol_table()[key])
    return tests


def find_symtable(symbol_table: Callable, cls_name: str) -> dict:
    """
    Retrieve a dictionary (object) starting with "Type_" from the symbol table.

    Args:
        symbol_table (Callable): A function that returns a symbol table dictionary ('globals', 'locals').
        cls_name (str): The name of the class whose associated types to find.

    Returns:
        dict: The found dictionary (object).

    Raises:
        KeyError: If the class whose associated types to find is not found in the symbol table.
    """
    type_name = "Type_" + cls_name
    try:
        return symbol_table()[type_name]  # E.g. globals()["Type_LuxuryCruise"]
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


def merge_rec(cls: dict, symbol_table: Callable) -> dict:
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
        result.update(merge_rec(cls["_parent"], symbol_table))
    result.update(cls)
    _type = find_symtable(symbol_table, result["_name"])
    result["_types"].update(_type)
    del result["_parent"]
    return result


def new(cls: dict, **kwargs) -> dict:
    """
    Instantiates a new dictionary containing all methods and attributes of the provided dictionary (class) and all its parents. Fills its attributes with the values provided via '**kwargs'.

    Args:
        cls (dict): The dictionary (class) to be instantiated.
        symbol_table (Callable, optional): The symbol table dictionary to reference ('globals', 'locals').
        **kwargs: Attributes to set on the new instance. If 'symbol_table' is not provided, it defaults to 'globals'.

    Returns:
        dict: The newly instantiated dictionary filled with the provided attributes.

    Raises:
        KeyError: If a required attribute is not provided in '**kwargs'.
        TypeError: If an attribute does not match the expected type.
    """
    if not "symbol_table" in kwargs:
        kwargs["symbol_table"] = globals
    merged_cls = merge_rec(cls, kwargs["symbol_table"])
    for key, value in merged_cls.items():
        if value is None:
            if not key in kwargs:
                raise KeyError(f"{key} must be provided")
            if not key in merged_cls:
                raise KeyError(f"{key} does not exist on {merged_cls['_name']}")
            merged_cls[key] = kwargs[key]
            _type = merged_cls["_types"][key]
            if not isinstance(kwargs[key], _type):
                raise TypeError(f"{key} must be a {_type}")
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
