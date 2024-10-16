from vacation_booking import * 

def run_tests(all_tests: list) -> None:
    """
    Runs each test in the list all_tests.

    Args:
        all_tests (list): The list with the test functions.

    Returns:
        None: it only prints the results of the tests.
    """
    results = {"pass": 0, "fail": 0, "error": 0}
    for test in all_tests:
        try:
            test()
            results["pass"] += 1
        except AssertionError:
            results["fail"] += 1
        except Exception as e:
            print(e)
            results["error"] += 1
    print(f"pass {results['pass']}")
    print(f"fail {results['fail']}")
    print(f"error {results['error']}")

def find_tests(prefix: str = "test_") -> list:
    """
    Finds all test functions whose names start with a given prefix.

    Args:
        prefix (str): The prefix of the test function names to search for.
                      Defaults to "test_".

    Returns:
        list: A list of test functions that match the given prefix.
    """
    tests = []
    for name, func in globals().items():
        if name.startswith(prefix):
           tests.append(func)
    return tests

def prevent_append(func: Callable) -> Callable:
    """
    Prevents appending an object to the global "booked_vacations" list during the execution of a function.

    Args:
        func (Callable): The function object in which we don't want to change "booked_vacations".

    Returns:
        Callable: The updated function with more functionality to prevent appending.
    """
    def wrapper(*args, **kwargs):
        original = globals()["booked_vacations"].copy()
        globals()['booked_vacations'].clear()
        try:
            func(*args, **kwargs)
        finally:
            globals()["booked_vacations"].extend(original)
    return wrapper

def create_sample_vacations() -> list:
    """
    Creates sample vacation objects (BeachResort, AdventureTrip, LuxuryCruise) to reduce repetitive code.

    Returns:
        list: A list of instantiated vacation objects (BeachResort, AdventureTrip, LuxuryCruise).
    """
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
    return [beach_resort, adventure_trip, luxury_cruise]


@prevent_append
def test_beachresort_calculatecost():
    """
    Tests the calculate_cost method for a BeachResort instance with surfing included.
    """
    beach_resort = new(
        BeachResort,
        destination="Maldives",
        cost_per_day=100,
        duration_in_days=7,
        include_surfing=True,
    )
    actual = call(beach_resort, "calculate_cost")
    expected = 7 * 100 + 100
    assert actual == expected

@prevent_append
def test_adventuretrip_calculatecost():
    """
    Tests the calculate_cost method for a AdventureTrip instance with an easy difficulty level.
    """
    adventure_trip = new(
        AdventureTrip,
        destination="Macchu Picchu",
        cost_per_day=150,
        duration_in_days=4,
        difficulty_level="easy",
    )
    actual = call(adventure_trip, "calculate_cost")
    expected = 150 * 4
    assert actual == expected

@prevent_append
def test_luxury_cruise_calculatecost():
    """
    Tests the calculate_cost method for a LuxuryCruise instance without a private suite.
    """
    luxury_cruise = new(
        LuxuryCruise,
        destination="Mediterranean",
        cost_per_day=100,
        duration_in_days=14,
        has_private_suite=False,
    )
    actual = call(luxury_cruise, "calculate_cost")
    expected = 100 * 14
    assert actual == expected

@prevent_append
def test_vacationbookingsummary_calculatecost():
    """
    Tests the calculate_cost method for VacationBookingSummary without passing "search_term".
    """
    create_sample_vacations()
    vacation_booking_summary = new(VacationBookingSummary)
    actual = call(vacation_booking_summary, "calculate_cost")
    expected = (7 * 100 + 100) + (150 * 4) + (100 * 14)
    assert actual == expected

if __name__ == "__main__":
    tests = find_tests()
    run_tests(tests)
