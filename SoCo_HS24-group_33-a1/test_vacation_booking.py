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