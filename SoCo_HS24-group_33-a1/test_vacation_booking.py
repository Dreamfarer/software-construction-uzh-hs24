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
    This test was chosen to ensure that the calculate_cost_beach_resort method is working properly.
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


def test_beach_resort_calculatecost_zero_days():
    """
    Tests the calculate_cost method for a beach resort instance with zero days
    and surfing included.
    This test was chosen to ensure that the edge case for a zero days duration of a BeachResort instance
    returns a total cost of zero and not 100.
    """
    beach_resort = new(
        BeachResort,
        destination = "Bali",
        cost_per_day = 188,
        duration_in_days = 0,
        include_surfing = True,
    )
    actual = call(beach_resort,"calculate_cost")
    expected = 0
    assert actual == expected


def test_adventure_trip_calculatecost():
    """
    Tests the calculate_cost method for a AdventureTrip instance with an easy difficulty level.
    This test was chosen to ensure that the calculate_cost_adventure method is working properly.
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
    This test was chosen to ensure that the calculate_cost_luxury_cruise method is working properly.
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


def test_luxury_cruise_calculatecost_zero_cost_per_day():
    """
    Tests the calculate_cost method for a LuxuryCruise instance with zero cost_per_day.
    This test was chosen to ensure that the total cost of a Vacation instance is zero if the cost_per_day
    attribute is 0.
    """
    luxury_cruise = new(
        LuxuryCruise,
        destination = "Hawaii",
        cost_per_day = 0,
        duration_in_days = 5,
        has_private_suite = False,
    )
    actual = call(luxury_cruise, "calculate_cost")
    expected = 0
    assert actual == expected


def test_vacationbookingsummary_calculatecost():
    """
    Tests the calculate_cost method for VacationBookingSummary without passing "search_term".
    This test was chosen to ensure that the total sum of all vacations instantiated are summed up correctly.
    """
    create_sample_vacations()
    vacation_booking_summary = new(VacationBookingSummary)
    actual = call(vacation_booking_summary, "calculate_cost")
    expected = (7 * 100 + 100) + (150 * 4) + (100 * 14)
    assert actual == expected


def test_describe_package_beach_resort():
    """
    Tests the describe_package method for a BeachResort instance with surfing included.
    This test was chosen to ensure that the describe_package_beach_resort method is working properly.
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
    This test was chosen to ensure that the describe_package_adventure method is working properly.
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
    This test was chosen to ensure that the describe_package_luxury_cruise method is working properly.
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
    This test was chosen that the extract_total_vacation_summary method is working properly without
    passing a search_term.
    """
    create_sample_vacations()
    vacation_booking_summary = new(VacationBookingSummary)
    actual = call(vacation_booking_summary,"describe_package")
    expected = "The 7 day long Beach Resort vacation in Maldives includes surfing.\nThe 4 day long Adventure trip in Macchu Picchu is considered easy.\nThe 14 day long Luxury Cruise in Mediterranean does not include a private suite."
    assert actual == expected


def test_vacationbookingsummary_describe_package_search_term():
    """
    Tests the desribe_package method for VacationBookingSummary with a search term Cruise.
    This test was chosen that the extract_total_vacation_summary method is working properly with
    passing a search_term.
    """
    create_sample_vacations()
    vacation_booking_summary = new(VacationBookingSummary, search_term = "Cruise")
    actual = call(vacation_booking_summary, "describe_package")
    expected = "The 14 day long Luxury Cruise in Mediterranean does not include a private suite."
    assert actual == expected


def test_vacationbooking_summary_invalid_search_term():
    """
    Tests the instantiation of VacationBookingSummary with an invalid type for search_term.
    This test was chosen that the extract_total_vacation_summary method is working properly with
    passing an invalid search_term. It tests the instantiation in the new function.
    """
    create_sample_vacations()
    try:
        vacation_booking_summary = new(VacationBookingSummary,search_term = 12)
        assert False, "TypeError not raised for invalid 'search_term' type"
    except TypeError:
        pass


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
    This test was chosen to test the type checking systems behaviour for passing an invalid type (float).
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
    """
    Tests the calculatecost method for an adventure instance with negative cost per day.
    This test was chosen to test the type checking systems behaviour for passing an invalid type (negative int)
    as well as the instantiation in the new function.
    """
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


def test_adventure_trip_invalid_difficulty_level():
    """
    Tests the instantiation of a AdventureTrip instance with an invalid difficulty level.
    This test was chosen to test the type checking systems behaviour for passing an invalid difficulty_level
    as well as the instantiation in the new function.
    """
    try:
        adventure_trip = new(
            AdventureTrip,
            destination = "Nigeria",
            cost_per_day = 300,
            duration_in_days = 4,
            difficulty_level = "medium",
        )
        assert False, "TypeError not raised"
    except TypeError:
        pass


def test_luxury_cruise_calculatecost_invalid_suite_type():
    """
    Tests the instantiation of a LuxuryCruise instance with an invalid suite type.
    This test was chosen to test the type checking systems behaviour for passing an invalid type(str)
    as well as the instantiation in the new function.
    """
    try:
        luxury_cruise = new(
            LuxuryCruise,
            destination = "Bora Bora",
            cost_per_day = 144,
            duration_in_days = 6,
            has_private_suite = "no",
        )
        assert False, "TypeError not raised"
    except TypeError:
        pass


def test_beach_resort_call_invalid_method_name():
    """
    Tests the find_cls method for a BeachResort instance with an invalid method_name.
    """
    beach_resort = new(
        BeachResort,
        destination = "Australia",
        cost_per_day = 65,
        duration_in_days = 6,
        include_surfing = True
    )
    try:
        call(beach_resort, "description")
        assert False, "KeyError not raised for invalid method call"
    except KeyError:
        pass


if __name__ == "__main__":
    tests = find_tests()
    run_tests(tests)
