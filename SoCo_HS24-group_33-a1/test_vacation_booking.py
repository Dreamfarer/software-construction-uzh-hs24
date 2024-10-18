from vacation_booking import *
import time
import argparse


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
    print(actual)
    expected = (7 * 100 + 100) + (150 * 4) + (100 * 14)
    assert actual == expected


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Run Tests for VacationBooking")
    parser.add_argument(
        "--select",
        type = str,
        default = None,
        help = "Only run tests with a specific pattern"
    )
    args = parser.parse_args()
    tests = find_tests(pattern = args.select)
    if not tests:
        print(f"No tests found matching the given pattern {args.select}")
        exit(1)
    run_tests(tests)
