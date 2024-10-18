from vacation_booking import *
import time


def run_tests(all_tests: list[Callable]) -> None:
    """
    Runs each test in the list all_tests, measures the time taken for each tests, and prints
    the results (pass, fail or error) along with the time taken.

    Args:
        all_tests (list): The list with the test functions.

    Returns:
        None: it only prints the results of the tests.
    """
    results = {"pass": 0, "fail": 0, "error": 0}

    for test in all_tests:
        global booked_vacations
        booked_vacations.clear()
        start_time = time.time()
        total_time = 0

        try:
            test()
            results["pass"] += 1
            result = "pass"
        except AssertionError:
            results["fail"] += 1
            result = "fail"
        except Exception as e:
            results["error"] += 1
            result = f"error {e}"
        finally:
            elapsed_time = time.time() - start_time
            print(f"{test.__name__}: {result} {elapsed_time:.3f} seconds")
            total_time += elapsed_time

    print(
        "------------------------------------------------\n"
        f"Ran {len(all_tests)} tests in {total_time:.3f}s\n"
        f"pass {results['pass']}\n"
        f"fail {results['fail']}\n"
        f"error {results['error']}"
    )


def find_tests(prefix: str = "test_") -> list[Callable]:
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


def create_sample_vacations() -> None:
    """
    Instantiate and append sample vacation objects (BeachResort, AdventureTrip, LuxuryCruise) to the global 'booked_vacations' list.
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


def test_beach_resort_calculatecost():
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


def test_adventure_trip_calculatecost():
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


def test_vacationbookingsummary_calculatecost():
    """
    Tests the calculate_cost method for VacationBookingSummary without passing "search_term".
    """
    create_sample_vacations()
    vacation_booking_summary = new(VacationBookingSummary)
    actual = call(vacation_booking_summary, "calculate_cost")
    expected = (7 * 100 + 100) + (150 * 4) + (100 * 14)
    assert actual == expected


def test_describe_package_beach_resort():
    """
    Tests the describe_package method for a BeachResort instance with surfing included.
    """
    beach_resort = new(
        BeachResort,
        destination = "Cuba",
        cost_per_day = 50,
        duration_in_days = 6,
        include_surfing = True
        )
    actual = call(beach_resort, "describe_package")
    expected = "The 6 day long Beach Resort vacation in Cuba includes surfing."
    assert actual == expected


def test_describe_package_adventure():
    """
    Tests the describe_package method for a adventureTrip instance with a hard difficulty level.
    """
    adventure_trip = new(
        AdventureTrip,
        destination = "Namibia",
        cost_per_day = 200,
        duration_in_days = 12,
        difficulty_level = "hard"
    )
    actual = call(adventure_trip, "describe_package")
    expected = "The 12 day long Adventure trip in Namibia is considered hard."
    assert actual == expected

def test_describe_package_luxury_cruise():
    """
    Tests the desribe_package method for a luxuryCurise instance with a private suite.
    """
    luxury_cruise = new(
        LuxuryCruise,
        destination = "Japan",
        cost_per_day = 67,
        duration_in_days = 8,
        has_private_suite = True
    )
    actual = call(luxury_cruise, "describe_package")
    expected = "The 8 day long Luxury Cruise in Japan does include a private suite."
    assert actual == expected


def test_vacationbookingsummary_describe_package():
    """
    Tests the describe_package method for VacationBookingSummary without passing "search_term".
    """
    create_sample_vacations()
    vacation_booking_summary = new(VacationBookingSummary)
    actual = call(vacation_booking_summary,"describe_package")
    expected = "The 7 day long Beach Resort vacation in Maldives includes surfing.\nThe 4 day long Adventure trip in Macchu Picchu is considered easy.\nThe 14 day long Luxury Cruise in Mediterranean does not include a private suite."
    assert actual == expected


def test_instantiation_missing_key():
    """
    Tests the new method for a vacation instance that misses a key. 
    """
    try:
        beach_resort = new(
        BeachResort,
        destination = "Italy",
        duration_in_days = 5,
        include_surfing = True
        )
        assert False, "KeyError not raised"
    except KeyError:
        pass

def test_beach_resort_calculatecost_float():
    """
    Tests the calculate_cost method for a BeachResort instance with a float number.
    """
    try:
        beach_resort = new(
            BeachResort,
            destination = "Bahamas",
            cost_per_day = 280.5,
            duration_in_days = 14,
            include_surfing = True
        )
        assert False, "TypeError not raised"
    except TypeError:
        pass


def test_adventure_calculate_cost_negative_int():
    try:
        adventure_trip = new(
            AdventureTrip,
            destination = "Switzerland",
            cost_per_day = -66,
            duration_in_days = 12,
            difficulty_level = "easy",
        )
        assert False, "TypeError not raised"
    except TypeError:
        pass

if __name__ == "__main__":
    tests = find_tests()
    run_tests(tests)
