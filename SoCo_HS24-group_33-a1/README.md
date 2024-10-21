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

## Test Documentation
...

## Code Documentation
...

## Disclaimer
We aimed to distribute the workload as evenly as possible, and overall, this was successful. However, the commit count varies due to different committing habits. Additionally, [Dreamfarer](https://gitlab.uzh.ch/Dreamfarer) handled most of the merge requests, resulting in a higher number of commits on his part.

ChatGPT was used as a tool to understand and learn concepts. However, all the code in this repository was authored exclusively by the three group members. ChatGPT contributed to writing docstrings and documentation, primarily for grammar correction and providing an outline.