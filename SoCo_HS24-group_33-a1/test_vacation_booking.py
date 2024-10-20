from vacation_booking import *
import time
import argparse

NAME_WIDTH = 75
RESULT_WIDTH = 8
TIME_WIDTH = 10

GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"
RESET = "\033[0m"


def print_results(
    outcome: str, name: str, time: float, exception: Exception = None
) -> None:

    space = " " * (NAME_WIDTH - len(name))
    output = name + space
    match outcome:
        case "pass":
            output += GREEN + "pass" + " " * (RESULT_WIDTH - 4)
        case "fail":
            output += YELLOW + "fail" + " " * (RESULT_WIDTH - 4)
        case "error":
            output += RED + "error" + " " * (RESULT_WIDTH - 5)
        case _:
            raise ValueError("Outcome must be either 'pass', 'fail' or 'error'.")
    output += RESET + f"{time:.3f}s"
    if exception:
        exception_type = type(exception).__name__
        exception_message = str(exception)
        output += " " * (TIME_WIDTH - 6) + f"[{exception_type}]: {exception_message}"
    print(output)


def run_tests(all_tests: list[Callable]) -> None:
    """
    Runs each test in the list all_tests, measures the time taken for each tests, and prints
    the results (pass, fail or error) along with the time taken.

    Args:
        all_tests (list): The list with the test functions.

    Returns:
        None: it only prints the results of the tests.
    """
    print(
        MAGENTA
        + "Name"
        + " " * (NAME_WIDTH - 4)
        + "Status"
        + " " * (RESULT_WIDTH - 6)
        + "Time"
        + " " * (TIME_WIDTH - 4)
        + "Error"
        + RESET
    )
    results = {"pass": 0, "fail": 0, "error": 0}
    total_time = 0
    for test in all_tests:
        global booked_vacations
        booked_vacations.clear()
        start_time = time.time()
        exception = None
        try:
            test()
            results["pass"] += 1
            result = "pass"
        except AssertionError:
            results["fail"] += 1
            result = "fail"
        except Exception as e:
            results["error"] += 1
            result = f"error"
            exception = e
        finally:
            elapsed_time = time.time() - start_time
            print_results(result, test.__name__, elapsed_time, exception)
            total_time += elapsed_time

    print(
        f"\n{MAGENTA}Ran {len(all_tests)} tests in {total_time:.3f}s\n"
        f"{GREEN}Pass:  {results['pass']}\n"
        f"{YELLOW}Fail:  {results['fail']}\n"
        f"{RED}Error: {results['error']}{RESET}"
    )


def find_tests(prefix: str = "test_", pattern: str = None) -> list[Callable]:
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
            if pattern is None or pattern.lower() in name.lower():
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


def test_adventure_trip_calculatecost_easy():
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


def test_adventure_trip_calculatecost_hard():
    """
    Tests the calculate_cost method for a AdventureTrip instance with a hard difficulty level.
    This test was chosen to ensure that the calculate_cost_adventure method is working properly.
    """
    adventure_trip = new(
        AdventureTrip,
        destination="Macchu Picchu",
        cost_per_day=150,
        duration_in_days=4,
        difficulty_level="hard",
    )
    actual = call(adventure_trip, "calculate_cost")
    expected = 150 * 4 * 2
    assert actual == expected


def test_beach_resort_calculatecost_with_surfing():
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


def test_beach_resort_calculatecost_without_surfing():
    """
    Tests the calculate_cost method for a BeachResort instance without surfing included.
    This test was chosen to ensure that the calculate_cost_beach_resort method is working properly.
    """
    beach_resort = new(
        BeachResort,
        destination="Maldives",
        cost_per_day=100,
        duration_in_days=7,
        include_surfing=False,
    )
    actual = call(beach_resort, "calculate_cost")
    expected = 7 * 100
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
        destination="Bali",
        cost_per_day=188,
        duration_in_days=0,
        include_surfing=True,
    )
    actual = call(beach_resort, "calculate_cost")
    expected = 0
    assert actual == expected


def test_luxury_cruise_calculatecost_with_suite():
    """
    Tests the calculate_cost method for a LuxuryCruise instance with a private suite.
    This test was chosen to ensure that the calculate_cost_luxury_cruise method is working properly.
    """
    luxury_cruise = new(
        LuxuryCruise,
        destination="Mediterranean",
        cost_per_day=100,
        duration_in_days=14,
        has_private_suite=True,
    )
    actual = call(luxury_cruise, "calculate_cost")
    expected = 100 * 14 * 1.5
    assert actual == expected


def test_luxury_cruise_calculatecost_without_suite():
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
        destination="Hawaii",
        cost_per_day=0,
        duration_in_days=5,
        has_private_suite=False,
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


def test_adventure_trip_describe_package():
    """
    Tests the describe_package method for a adventureTrip instance with a hard difficulty level.
    This test was chosen to ensure that the describe_package_adventure method is working properly.
    """
    adventure_trip = new(
        AdventureTrip,
        destination="Namibia",
        cost_per_day=200,
        duration_in_days=12,
        difficulty_level="hard",
    )
    actual = call(adventure_trip, "describe_package")
    expected = "The 12 day long Adventure trip in Namibia is considered hard."
    assert actual == expected


def test_beach_resort_describe_package():
    """
    Tests the describe_package method for a BeachResort instance with surfing included.
    This test was chosen to ensure that the describe_package_beach_resort method is working properly.
    """
    beach_resort = new(
        BeachResort,
        destination="Cuba",
        cost_per_day=50,
        duration_in_days=6,
        include_surfing=True,
    )
    actual = call(beach_resort, "describe_package")
    expected = "The 6 day long Beach Resort vacation in Cuba includes surfing."
    assert actual == expected


def test_luxury_cruise_describe_package():
    """
    Tests the desribe_package method for a luxuryCurise instance with a private suite.
    This test was chosen to ensure that the describe_package_luxury_cruise method is working properly.
    """
    luxury_cruise = new(
        LuxuryCruise,
        destination="Japan",
        cost_per_day=67,
        duration_in_days=8,
        has_private_suite=True,
    )
    actual = call(luxury_cruise, "describe_package")
    expected = "The 8 day long Luxury Cruise in Japan does include a private suite."
    assert actual == expected


def test_vacationbookingsummary_describe_package():
    """
    Tests the describe_package method for VacationBookingSummary without passing "search_term".
    This test was chosen to ensure that the extract_total_vacation_summary method is working properly without
    passing a search_term.
    """
    create_sample_vacations()
    vacation_booking_summary = new(VacationBookingSummary)
    actual = call(vacation_booking_summary, "describe_package")
    expected = "The 7 day long Beach Resort vacation in Maldives includes surfing.\nThe 4 day long Adventure trip in Macchu Picchu is considered easy.\nThe 14 day long Luxury Cruise in Mediterranean does not include a private suite."
    assert actual == expected


def test_vacationbookingsummary_describe_package_search_term():
    """
    Tests the desribe_package method for VacationBookingSummary with a search term Cruise.
    This test was chosen to ensure that the extract_total_vacation_summary method is working properly with
    passing a search_term.
    """
    create_sample_vacations()
    vacation_booking_summary = new(VacationBookingSummary, search_term="Cruise")
    actual = call(vacation_booking_summary, "describe_package")
    expected = "The 14 day long Luxury Cruise in Mediterranean does not include a private suite."
    assert actual == expected


def test_vacationbookingsummary_describe_package_no_matching_search_term():
    """
    Tests the instantiation of VacationBookingSummary with a search_term not matching any vacation.
    This test was chosen to ensure that the extract_total_vacation_summary method is working properly with
    passing an invalid search_term. It tests the instantiation in the new function.
    """
    create_sample_vacations()
    vacation_booking_summary = new(
        VacationBookingSummary, search_term="non_existing_vacation"
    )
    actual = call(vacation_booking_summary, "describe_package")
    expected = ""
    assert actual == expected


def test_instantiation_missing_key():
    """
    Tests the new method for a vacation instance that misses a key.
    This test was chosen to ensure that the new method raises KeyError if an argument is missing in the constructor.
    """
    try:
        beach_resort = new(
            BeachResort, destination="Italy", duration_in_days=5, include_surfing=True
        )
        assert False, "KeyError not raised"
    except KeyError:
        pass


def test_instantiation_too_many_key():
    """
    Tests the new method for a vacation instance that has one more extra key.
    This test was chosen to ensure that the new method raises KeyError if there an extra argument was passed to the new method.
    """
    try:
        beach_resort = new(
            BeachResort,
            destination="Italy",
            cost_per_day=50,
            duration_in_days=5,
            include_surfing=True,
            extra_key="extra",
        )
        assert False, "KeyError not raised"
    except KeyError:
        pass


def test_adventure_trip_calculate_cost_negative_int():
    """
    Tests the calculatecost method for an adventure instance with negative cost per day.
    This test was chosen to test the behaviour of the type checking system when passing an invalid cost_per_day (negative int)
    as well as the instantiation in the new function.
    """
    try:
        adventure_trip = new(
            AdventureTrip,
            destination="Switzerland",
            cost_per_day=-66,
            duration_in_days=12,
            difficulty_level="easy",
        )
        assert False, "TypeError not raised"
    except TypeError:
        pass


def test_adventure_trip_invalid_difficulty_level():
    """
    Tests the instantiation of a AdventureTrip instance with an invalid difficulty level.
    This test was chosen to test the behaviour of the type checking system when passing an invalid difficulty_level
    as well as the instantiation in the new function.
    """
    try:
        adventure_trip = new(
            AdventureTrip,
            destination="Nigeria",
            cost_per_day=300,
            duration_in_days=4,
            difficulty_level="medium",
        )
        assert False, "TypeError not raised"
    except TypeError:
        pass


def test_beach_resort_invalid_include_surfing():
    """
    Tests the TypeError in the new method when passing an invalid include_surfing type
    This test was chosen to test the behaviour of the type checking system when passing an invalid include_surfing
    as well as the instantiation in the new function.
    """
    try:
        beach_resort = new(
            BeachResort,
            destination="Bahamas",
            cost_per_day=100,
            duration_in_days=14,
            include_surfing="10",
        )
        assert False, "TypeError not raised"
    except TypeError:
        pass


def test_luxury_cruise_calculatecost_invalid_suite_type():
    """
    Tests the instantiation of a LuxuryCruise instance with an invalid suite type.
    This test was chosen to test the behaviour of the type checking system when passing an invalid has_private_suite
    as well as the instantiation in the new function.
    """
    try:
        luxury_cruise = new(
            LuxuryCruise,
            destination="Bora Bora",
            cost_per_day=144,
            duration_in_days=6,
            has_private_suite="no",
        )
        assert False, "TypeError not raised"
    except TypeError:
        pass


def test_vacationbookingsummary_invalid_search_term():
    """
    Tests the instantiation of VacationBookingSummary with an invalid type for search_term.
    This test was chosen to test the behaviour of the type checking system when passing an invalid search_term
    as well as the instantiation in the new function.
    """
    create_sample_vacations()
    try:
        vacation_booking_summary = new(VacationBookingSummary, search_term=12)
        assert False, "TypeError not raised for invalid 'search_term' type"
    except TypeError:
        pass


def test_call_invalid_method_name():
    """
    Tests the find_cls method for a BeachResort instance with an invalid method_name.
    This test was chosen to ensure that the call function raises KeyError when passing a non existing method.
    """
    beach_resort = new(
        BeachResort,
        destination="Australia",
        cost_per_day=65,
        duration_in_days=6,
        include_surfing=True,
    )
    try:
        call(beach_resort, "description")
        assert False, "KeyError not raised for invalid method call"
    except KeyError:
        pass


def test_call_too_many_arguments():
    """
    Tests the call method for a BeachResort instance with an extra argument
    This test was chosen to ensure that the call function raises TypeError when passing an extra argument than needed for the corresponding method.
    """
    beach_resort = new(
        BeachResort,
        destination="Australia",
        cost_per_day=65,
        duration_in_days=6,
        include_surfing=True,
    )
    try:
        call(beach_resort, "describe_package", "extra")
        assert (
            False
        ), "TypeError was not raised when calling a method with an extra argument"
    except TypeError:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Tests for VacationBooking")
    parser.add_argument(
        "-s",
        "--select",
        default=None,
        help="only run tests with a specific pattern",
    )
    args = parser.parse_args()
    tests = find_tests(pattern=args.select)
    if not tests:
        print(f"No tests found matching the given pattern '{args.select}'!")
        exit(1)
    run_tests(tests)
