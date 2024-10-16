from vacation_booking import * 

def run_tests(all_tests: list) -> None:
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
    tests = []
    for name, func in globals().items():
        if name.startswith(prefix):
           tests.append(func)
    return tests

def prevent_append(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        original = globals()["booked_vacations"].copy()
        globals()['booked_vacations'].clear()
        try:
            func(*args, **kwargs)
        finally:
            globals()["booked_vacations"].extend(original)
    return wrapper

def create_sample_vacations() -> list:
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