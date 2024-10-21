# GROUP33 – Software Construction HS24 Task I
**Building an Object System, Type Enforcement, and Testing Framework – Without the `class` Keyword**\
*By Ceyhun, Gianluca and Mischa*

## Table of Contents
- [Overview](#overview): Explanation and design decisions
- [Test Documentation](#test-documentation): Detailed overview of each test
- [Code Documentation](#code-documentation): Detailed overview of each method
- [Disclaimer](#disclaimer): Use of AI tools and commit distribution explanation

## Overview
This section outlines our general approach and the rationale behind key design decisions. For method-specific details, please refer to the [Code Documentation](#code-documentation). For details on the tests in the testing framework, see [Test Documentation](#test-documentation).

#### Mocking Classes
We chose to represent classes using dictionaries, as they best mimic the structure and behavior of real Python classes among built-in options. Each dictionary (referred to as a 'class') contains at least the following attributes:
* Parent (`_parent`): We implemented inheritance using the `_parent` attribute, allowing child classes to reuse functionality from parent classes. This reduces code duplication and follows object-oriented programming principles. It also supports overriding methods or attributes, similar to traditional class behavior.
* Type (`_types`): The `_types` dictionary enforces type and value constraints for attributes and methods, ensuring data integrity by validating that only correct data is assigned. This approach allows us to catch potential errors early. Our implementation is inspired by TypeScript's Interfaces.
* Name (`_name`): The `_name` attribute serves as an identifier within the symbol table, making it easier to reference instances and their type restrictions.

Additional attributes and methods can be added as needed. Below is an example showing the implementation of `AdventureTrip`, which inherits from `VacationPackage` (and thereby from `Class`):
```
Class = {"_parent": None, "_name": "Class", "_types": {}}
```
```
VacationPackage = {
    "_parent": Class,
    "_name": "VacationPackage",
    "calculate_cost": None,
    "describe_package": None,
    "destination": None,
    "cost_per_day": None,
    "duration_in_days": None,
}
```
```
AdventureTrip = {
    "_parent": VacationPackage,
    "_name": "AdventureTrip",
    "calculate_cost": calculate_cost_adventure,
    "describe_package": describe_package_adventure,
    "difficulty_level": None,
}
```
Each class must be accompanied by a dictionary that specifies its type and value constraints. Continuing from the example above, here are the corresponding type dictionaries:
```
Type_Class = {"_parent": str, "_name": str, "_types": dict}
```
```
Type_VacationPackage = {
    "_parent": dict,
    "_name": str,
    "calculate_cost": Callable,
    "describe_package": Callable,
    "destination": str,
    "cost_per_day": lambda x: isinstance(x, int) and x >= 0,
    "duration_in_days": int,
}
```
```
Type_AdventureTrip = {
    "difficulty_level": ["easy", "hard"],
}
```

#### Creating a New Instance
We handle object instantiation through the `new()` method. It first merges attributes and methods from parent classes recursively using `merge_rec()`, creating a new instance. Then, the parameters passed to `new()` are validated against the class’s type and value restrictions. If valid, these parameters override the default values and the newly created object is added to a global list (`booked_vacations`) containing all booked vacations. This approach avoids complex nested dictionaries and ensures the simplicity and clarity of instance representations. Validation during instantiation helps to prevent invalid data from entering the system.

Here's an example of creating a new instance of the `AdventureTrip` class:

```
adventure_trip = new(
    AdventureTrip,
    destination="Macchu Picchu",
    cost_per_day=150,
    duration_in_days=4,
    difficulty_level="easy",
)
```

#### Calling Methods
The `call()` function is used to invoke methods on objects, mimicking how methods are called in actual Python classes. Below is an example of how to call `adventure_trip.calculate_cost()` in actual Python classes:
```
call(adventure_trip, "calculate_cost")
```

#### Testing Framework
Before running tests, our framework identifies all methods in the global symbol table that start with the prefix `test_` using the find_tests() method. It then iterates through each test with `run_tests()`, measuring the time taken for each test, and prints the results (pass, fail, or error) along with the execution time using `print_results()`. We chose this symbol table approach so that we don't need to manually track all the written tests.

Refer to [Test Documentation](#test-documentation) for detailed descriptions and explanations of each test.

## Code Documentation

<a id="vacation_booking.find_symtable"></a>

#### find\_symtable

```python
def find_symtable(cls_name: str) -> dict
```

Retrieve a dictionary (object) starting with "Type_" from the global symbol table.

**Arguments**:

- `cls_name` _str_ - The name of the class whose associated types to find.
  

**Returns**:

- `dict` - The found dictionary (object).
  

**Raises**:

- `KeyError` - If the class whose associated types to find is not found in the global symbol table.

<a id="vacation_booking.find_cls"></a>

#### find\_cls

```python
def find_cls(cls: dict, method_name: str) -> Callable
```

Find a method inside the dictionary (object) and return it.

**Arguments**:

- `cls` _dict_ - The dictionary (object) in which to find the method.
- `method_name` _str_ - The name of the method to be found.
  

**Returns**:

- `Callable` - The found method.
  

**Raises**:

- `KeyError` - If the method is not found in the dictionary.

<a id="vacation_booking.call"></a>

#### call

```python
def call(cls: dict, method_name: str, *args) -> any
```

Execute the specified method on the given dictionary (object) and return its result.

**Arguments**:

- `cls` _dict_ - The dictionary (object) on which to call the method.
- `method_name` _str_ - The name of the method to be called.
- `*args` - Additional arguments to pass to the method.
  

**Returns**:

- `Any` - The return value of the executed method.

<a id="vacation_booking.merge_rec"></a>

#### merge\_rec

```python
def merge_rec(cls: dict) -> dict
```

Recursively merge the methods and attributes of a dictionary (class) with those of its parent.
Additionally, update the '_types' key with type information from the symbol table based on the class name.

**Arguments**:

- `cls` _dict_ - The dictionary (class) to be instantiated.
- `symbol_table` _Callable_ - A function that returns a symbol table dictionary ('globals', 'locals').
  

**Returns**:

- `dict` - The newly instantiated dictionary (object) with merged attributes, methods and type information.

<a id="vacation_booking.is_valid_kwarg"></a>

#### is\_valid\_kwarg

```python
def is_valid_kwarg(cls: dict, kwargs: dict, key: str) -> bool
```

Checks whether the given key in the provided keyword arguments 'kwargs' is valid based on the rules defined in the '_types' dictionary of the provided dictionary (class) 'cls'.

**Arguments**:

- `cls` _dict_ - The before instantiated dictionary (class) 'cls'.
- `kwargs` _dict_ - A dictionary containing keyword arguments to validate.
- `key` _str_ - A single key from the before instantiated dictionary (class) 'cls'.
  

**Returns**:

- `bool` - Returns 'True' if the provided keyword argument passes all validation checks. Returns 'False' if the key is already set in 'cls' and no keyword argument in 'kwargs' is provided to modify it.
  

**Raises**:

- `KeyError` - If the key is required (set to 'None' in 'cls') but is not found in 'kwargs'.
- `KeyError` - If the key in 'kwargs' is not a valid key in the 'cls' dictionary.
- `TypeError` - If the value of the key in 'kwargs' is not of the expected type as specified by 'cls['_types'][key]'.
- `TypeError` - If a custom validation function in 'cls['_types'][key]' fails.

<a id="vacation_booking.new"></a>

#### new

```python
def new(cls: dict, **kwargs) -> dict
```

Instantiates a new dictionary containing all methods and attributes of the provided dictionary (class) and all its parents. Fills its attributes with the values provided via '**kwargs'.

**Arguments**:

- `cls` _dict_ - The dictionary (class) to be instantiated.
- `**kwargs` - Attributes to set on the new instance.


**Returns**:

- `dict` - The newly instantiated dictionary filled with the provided attributes.
  

**Raises**:

- `KeyError` - If a required attribute is not provided in '**kwargs'.
- `TypeError` - If an attribute does not match the expected type.

#### run\_tests

```python
def run_tests(all_tests: list[Callable]) -> None
```

Runs each test in the list all_tests, measures the time taken for each tests, and prints
the results (pass, fail or error) along with the time taken.

**Arguments**:

- `all_tests` _list_ - The list with the test functions.
  

**Returns**:

- `None` - it only prints the results of the tests.

<a id="test_vacation_booking.find_tests"></a>

#### find\_tests

```python
def find_tests(prefix: str = "test_", pattern: str = None) -> list[Callable]
```

Finds all test functions whose names start with a given prefix.

**Arguments**:

- `prefix` _str_ - The prefix of the test function names to search for.
  Defaults to "test_".
  

**Returns**:

- `list` - A list of test functions that match the given prefix.

<a id="test_vacation_booking.create_sample_vacations"></a>

#### create\_sample\_vacations

```python
def create_sample_vacations() -> None
```

Instantiate and append sample vacation objects (BeachResort, AdventureTrip, LuxuryCruise) to the global 'booked_vacations' list.

## Test Documentation
<a id="test_vacation_booking.test_adventure_trip_calculatecost_easy"></a>

#### test\_adventure\_trip\_calculatecost\_easy

```python
def test_adventure_trip_calculatecost_easy()
```

Tests the calculate_cost method for a AdventureTrip instance with an easy difficulty level.
This test was chosen to ensure that the calculate_cost_adventure method is working properly.

<a id="test_vacation_booking.test_adventure_trip_calculatecost_hard"></a>

#### test\_adventure\_trip\_calculatecost\_hard

```python
def test_adventure_trip_calculatecost_hard()
```

Tests the calculate_cost method for a AdventureTrip instance with a hard difficulty level.
This test was chosen to ensure that the calculate_cost_adventure method is working properly.

<a id="test_vacation_booking.test_beach_resort_calculatecost_with_surfing"></a>

#### test\_beach\_resort\_calculatecost\_with\_surfing

```python
def test_beach_resort_calculatecost_with_surfing()
```

Tests the calculate_cost method for a BeachResort instance with surfing included.
This test was chosen to ensure that the calculate_cost_beach_resort method is working properly.

<a id="test_vacation_booking.test_beach_resort_calculatecost_without_surfing"></a>

#### test\_beach\_resort\_calculatecost\_without\_surfing

```python
def test_beach_resort_calculatecost_without_surfing()
```

Tests the calculate_cost method for a BeachResort instance without surfing included.
This test was chosen to ensure that the calculate_cost_beach_resort method is working properly.

<a id="test_vacation_booking.test_beach_resort_calculatecost_zero_days"></a>

#### test\_beach\_resort\_calculatecost\_zero\_days

```python
def test_beach_resort_calculatecost_zero_days()
```

Tests the calculate_cost method for a beach resort instance with zero days
and surfing included.
This test was chosen to ensure that the edge case for a zero days duration of a BeachResort instance
returns a total cost of zero and not 100.

<a id="test_vacation_booking.test_luxury_cruise_calculatecost_with_suite"></a>

#### test\_luxury\_cruise\_calculatecost\_with\_suite

```python
def test_luxury_cruise_calculatecost_with_suite()
```

Tests the calculate_cost method for a LuxuryCruise instance with a private suite.
This test was chosen to ensure that the calculate_cost_luxury_cruise method is working properly.

<a id="test_vacation_booking.test_luxury_cruise_calculatecost_without_suite"></a>

#### test\_luxury\_cruise\_calculatecost\_without\_suite

```python
def test_luxury_cruise_calculatecost_without_suite()
```

Tests the calculate_cost method for a LuxuryCruise instance without a private suite.
This test was chosen to ensure that the calculate_cost_luxury_cruise method is working properly.

<a id="test_vacation_booking.test_luxury_cruise_calculatecost_zero_cost_per_day"></a>

#### test\_luxury\_cruise\_calculatecost\_zero\_cost\_per\_day

```python
def test_luxury_cruise_calculatecost_zero_cost_per_day()
```

Tests the calculate_cost method for a LuxuryCruise instance with zero cost_per_day.
This test was chosen to ensure that the total cost of a Vacation instance is zero if the cost_per_day
attribute is 0.

<a id="test_vacation_booking.test_vacationbookingsummary_calculatecost"></a>

#### test\_vacationbookingsummary\_calculatecost

```python
def test_vacationbookingsummary_calculatecost()
```

Tests the calculate_cost method for VacationBookingSummary without passing "search_term".
This test was chosen to ensure that the total sum of all vacations instantiated are summed up correctly.

<a id="test_vacation_booking.test_adventure_trip_describe_package"></a>

#### test\_adventure\_trip\_describe\_package

```python
def test_adventure_trip_describe_package()
```

Tests the describe_package method for a adventureTrip instance with a hard difficulty level.
This test was chosen to ensure that the describe_package_adventure method is working properly.

<a id="test_vacation_booking.test_beach_resort_describe_package"></a>

#### test\_beach\_resort\_describe\_package

```python
def test_beach_resort_describe_package()
```

Tests the describe_package method for a BeachResort instance with surfing included.
This test was chosen to ensure that the describe_package_beach_resort method is working properly.

<a id="test_vacation_booking.test_luxury_cruise_describe_package"></a>

#### test\_luxury\_cruise\_describe\_package

```python
def test_luxury_cruise_describe_package()
```

Tests the desribe_package method for a luxuryCurise instance with a private suite.
This test was chosen to ensure that the describe_package_luxury_cruise method is working properly.

<a id="test_vacation_booking.test_vacationbookingsummary_describe_package"></a>

#### test\_vacationbookingsummary\_describe\_package

```python
def test_vacationbookingsummary_describe_package()
```

Tests the describe_package method for VacationBookingSummary without passing "search_term".
This test was chosen to ensure that the extract_total_vacation_summary method is working properly without
passing a search_term.

<a id="test_vacation_booking.test_vacationbookingsummary_describe_package_search_term"></a>

#### test\_vacationbookingsummary\_describe\_package\_search\_term

```python
def test_vacationbookingsummary_describe_package_search_term()
```

Tests the desribe_package method for VacationBookingSummary with a search term Cruise.
This test was chosen to ensure that the extract_total_vacation_summary method is working properly with
passing a search_term.

<a id="test_vacation_booking.test_vacationbookingsummary_describe_package_no_matching_search_term"></a>

#### test\_vacationbookingsummary\_describe\_package\_no\_matching\_search\_term

```python
def test_vacationbookingsummary_describe_package_no_matching_search_term()
```

Tests the instantiation of VacationBookingSummary with a search_term not matching any vacation.
This test was chosen to ensure that the extract_total_vacation_summary method is working properly with
passing an invalid search_term. It tests the instantiation in the new function.

<a id="test_vacation_booking.test_instantiation_missing_key"></a>

#### test\_instantiation\_missing\_key

```python
def test_instantiation_missing_key()
```

Tests the new method for a vacation instance that misses a key.
This test was chosen to ensure that the new method raises KeyError if an argument is missing in the constructor.

<a id="test_vacation_booking.test_instantiation_too_many_key"></a>

#### test\_instantiation\_too\_many\_key

```python
def test_instantiation_too_many_key()
```

Tests the new method for a vacation instance that has one more extra key.
This test was chosen to ensure that the new method raises KeyError if there an extra argument was passed to the new method.

<a id="test_vacation_booking.test_adventure_trip_calculate_cost_negative_int"></a>

#### test\_adventure\_trip\_calculate\_cost\_negative\_int

```python
def test_adventure_trip_calculate_cost_negative_int()
```

Tests the calculatecost method for an adventure instance with negative cost per day.
This test was chosen to test the behaviour of the type checking system when passing an invalid cost_per_day (negative int)
as well as the instantiation in the new function.

<a id="test_vacation_booking.test_adventure_trip_invalid_difficulty_level"></a>

#### test\_adventure\_trip\_invalid\_difficulty\_level

```python
def test_adventure_trip_invalid_difficulty_level()
```

Tests the instantiation of a AdventureTrip instance with an invalid difficulty level.
This test was chosen to test the behaviour of the type checking system when passing an invalid difficulty_level
as well as the instantiation in the new function.

<a id="test_vacation_booking.test_beach_resort_invalid_include_surfing"></a>

#### test\_beach\_resort\_invalid\_include\_surfing

```python
def test_beach_resort_invalid_include_surfing()
```

Tests the TypeError in the new method when passing an invalid include_surfing type
This test was chosen to test the behaviour of the type checking system when passing an invalid include_surfing
as well as the instantiation in the new function.

<a id="test_vacation_booking.test_luxury_cruise_calculatecost_invalid_suite_type"></a>

#### test\_luxury\_cruise\_calculatecost\_invalid\_suite\_type

```python
def test_luxury_cruise_calculatecost_invalid_suite_type()
```

Tests the instantiation of a LuxuryCruise instance with an invalid suite type.
This test was chosen to test the behaviour of the type checking system when passing an invalid has_private_suite
as well as the instantiation in the new function.

<a id="test_vacation_booking.test_vacationbookingsummary_invalid_search_term"></a>

#### test\_vacationbookingsummary\_invalid\_search\_term

```python
def test_vacationbookingsummary_invalid_search_term()
```

Tests the instantiation of VacationBookingSummary with an invalid type for search_term.
This test was chosen to test the behaviour of the type checking system when passing an invalid search_term
as well as the instantiation in the new function.

<a id="test_vacation_booking.test_call_invalid_method_name"></a>

#### test\_call\_invalid\_method\_name

```python
def test_call_invalid_method_name()
```

Tests the find_cls method for a BeachResort instance with an invalid method_name.
This test was chosen to ensure that the call function raises KeyError when passing a non existing method.

<a id="test_vacation_booking.test_call_too_many_arguments"></a>

#### test\_call\_too\_many\_arguments

```python
def test_call_too_many_arguments()
```

Tests the call method for a BeachResort instance with an extra argument
This test was chosen to ensure that the call function raises TypeError when passing an extra argument than needed for the corresponding method.

## Disclaimer
We aimed to distribute the workload as evenly as possible, and overall, this was successful. However, the commit count varies due to different committing habits. Additionally, [Dreamfarer](https://gitlab.uzh.ch/Dreamfarer) handled most of the merge requests, resulting in a higher number of commits on his part.

ChatGPT was used as a tool to understand and learn concepts. However, all the code in this repository was authored exclusively by the three group members. ChatGPT contributed to writing docstrings and documentation, primarily for grammar correction and providing an outline.