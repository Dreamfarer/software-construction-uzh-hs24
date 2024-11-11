# GROUP33 – Software Construction HS24 Task II
**Extend the Little German Language (LGL) interpreter by adding support for infix and boolean expressions, lexical scoping, and tracing**\
*By Ceyhun, Gianluca and Mischa*

## Table of Contents
- [Overview](#overview): Explanation and design decisions
- [Disclaimer](#disclaimer): Use of AI tools, Python requirements and commit distribution explanation
- [Interpreter Documentation](#interpreter-documentation): Detailed overview of each method in `lgl_interpreter.py`
- [Reporting Documentation](#reporting-documentation): Detailed overview of each method in `reporting.py`

## Overview
This section outlines our general approach and the rationale behind key design decisions. For method-specific details, please refer to the [Code Documentation](#code-documentation).

#### LGL as A Tree Structure
We quickly realized that the Little German Language (LGL) can essentially be represented as a tree, with atomic expressions acting as leaves. Operations like `do_set`, `do_get`, `do_add`, and others serve as tree nodes, each with a specific (fixed for most, except `seq`) number of branches. Our `do` method manages this tree, determining which branches to append. `do` receives the entire LGL code and processes it in a depth-first manner, dividing and conquering the structure as it goes.

#### Infix Arithmetic and Boolean Operations
Since infix notation simply means that the operation identifier appears between operands, unlike prefix notation where the operation identifier appears first, we decided to convert infix instructions to prefix form before processing. The Boolean operations are structurally similar to the arithmetic operations already implemented, so adding them was trivial. For a detailed description of each operation, please refer to the [Code Documentation](#code-documentation).

#### Functions
To improve readability and understanding, we implemented a `Function` class to represent functions. Each `Function` object holds parameters, a body, and the current frame. The `do_function` method creates new functions, while `do_call` invokes the `call` method of the `Function` object. This, in turn, adds parameters as variables to the current frame and calls `do` on the current frame with the function body.

#### Lexical Scoping with Frames
Our implementation mimics Python's lexical scoping through a custom `Frame` class. The `do_set` method adds variables and functions to the current frame, while `do_get` retrieves them, checking the current frame first and then recursively searching parent frames if needed. Each time a new function is defined, a new frame is created with the current frame as its parent, allowing for **nested function definitions**. This modular approach also enables easy switching to dynamic scoping: simply open a new frame when calling functions instead of when defining them.

#### Tracing
We implemented tracing with a `Trace` class, utilizing a mix of object and class variables and methods. Each function that includes `@Trace.decorate` as a decorator logs its name, unique ID (a hash of the function name and definition timestamp), and precise start and end times to the class variable `call_stack`. Timing is measured using a combination of `datetime` and `perf_counter` to ensure maximum precision. Users can call `write` to generate a `.csv` file of the current call stack as needed.

#### Reporting
Reporting consists of two steps. First, `parse_log` processes the `.csv` output from `Trace.write`, organizing it into a dictionary where each function name serves as a key, and the associated value is another dictionary containing the number of calls and total time consumed. Then, `print_results` formats and displays this dictionary in the desired output format.

## Disclaimer
We aimed to distribute the workload as evenly as possible, and overall, this was successful. However, the commit count varies due to different committing habits. Additionally, [Dreamfarer](https://gitlab.uzh.ch/Dreamfarer) handled most of the merge requests, resulting in a higher number of commits on his part.

Please note that since our implementation uses `match` (the switch case of Python), Python >= 3.10 is **required** to run this code error-free.

ChatGPT was used as a tool to understand and learn concepts. However, all the code in this repository that extends the Little German Language (LGL) interpreter was authored exclusively by the three group members. ChatGPT contributed to writing docstrings and documentation, primarily for grammar correction and providing an outline.

## Interpreter Documentation

<a id="lgl_interpreter.Frame"></a>

## Frame Objects

```python
class Frame()
```

Mimics real Python frames (environments), enabling nested function definitions.

<a id="lgl_interpreter.Frame.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent: "Frame" = None) -> None
```

Initializes a new frame with an optional parent frame.

**Arguments**:

- `parent` _Frame, optional_ - The parent frame. Defaults to None.

<a id="lgl_interpreter.Frame.get"></a>

#### get

```python
def get(var_name: str) -> any
```

Retrieves the value of a variable with the given name from the current frame.
If not found, searches recursively in parent frames.

**Arguments**:

- `var_name` _str_ - The name of the variable to find.


**Returns**:

- `any` - The value of the found variable.


**Raises**:

- `KeyError` - If the variable is not found in the current or any parent frame.

<a id="lgl_interpreter.Frame.add"></a>

#### add

```python
def add(name: str, value: any) -> None
```

Adds a new variable with the given name and value to the current frame.

**Arguments**:

- `name` _str_ - The name of the variable.
- `value` _any_ - The value of the variable.


**Returns**:

  None

<a id="lgl_interpreter.Function"></a>

## Function Objects

```python
class Function()
```

Imitates a Python function. This class holds the function's parameters, body, and frame, which contains variables and other functions defined within this function. It also implements the callability of the 'Function' object.

<a id="lgl_interpreter.Function.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parameters: str | list[str], body: list, frame: Frame) -> None
```

Initializes a Function instance with parameters, body, and a frame.

**Arguments**:

- `parameters` _str | list[str]_ - The parameters of the function
- `body` _list_ - The body of the function, represented as a list of expressions.
- `frame` _Frame_ - The frame in which the function's variables and nested functions are defined.

<a id="lgl_interpreter.Function.call"></a>

#### call

```python
def call(evaluated_args: list[int]) -> any
```

Calls this 'Function' object. Adds the parameters as variables to the current frame and evaluates the function body in the current frame.

**Arguments**:

- `evaluated_args` _list[int]_ - A list of evaluated expressions to assign to the function parameters.


**Returns**:

- `any` - The result of evaluating the function's body.

<a id="lgl_interpreter.Trace"></a>

## Trace Objects

```python
class Trace()
```

Handles functionality for tracing the call stack. Provides a decorator '@Trace.decorate'
that logs entries to the call stack when functions start and stop execution.

<a id="lgl_interpreter.Trace.__init__"></a>

#### \_\_init\_\_

```python
def __init__(function_name: str) -> None
```

Initializes a Trace instance with a unique ID and the function name.

**Arguments**:

- `function_name` _str_ - The name of the function being traced.

<a id="lgl_interpreter.Trace.decorate"></a>

#### decorate

```python
@staticmethod
def decorate(func: callable) -> callable
```

Decorator to wrap functions with trace logging. Adds an entry to the call stack
whenever the decorated function starts and stops executing.

**Arguments**:

- `func` _callable_ - The function to be wrapped and traced.


**Returns**:

- `callable` - The wrapped function with trace logging.

<a id="lgl_interpreter.Trace.write"></a>

#### write

```python
@classmethod
def write(cls, file_path: str) -> None
```

Logs the call stack to a specified .csv file.

**Arguments**:

- `file_path` _str_ - The file path where the call stack should be logged.


**Returns**:

  None

<a id="lgl_interpreter.Trace.add"></a>

#### add

```python
def add(event: str) -> None
```

Adds an event to the call stack.

**Arguments**:

- `event` _str_ - The event type, such as 'start' or 'stop'.


**Returns**:

  None

<a id="lgl_interpreter.do_add"></a>

#### do\_add

```python
def do_add(frame: Frame, args: list) -> int
```

Adds two evaluated values: a + b.

**Arguments**:

- `frame` _Frame_ - The current execution frame.
- `args` _list_ - A list containing two integers to add. Each integer can be a direct value or an expression that requires evaluation.


**Returns**:

- `int` - The result of adding the two evaluated values.

<a id="lgl_interpreter.do_subtract"></a>

#### do\_subtract

```python
def do_subtract(frame: Frame, args: list) -> int
```

Subtracts two evaluated values: a - b.

**Arguments**:

- `frame` _Frame_ - The current execution frame.
- `args` _list_ - A list containing two integers to subtract. Each integer can be a direct value or an expression that requires evaluation.


**Returns**:

- `int` - The result of subtracting the two evaluated values.

<a id="lgl_interpreter.do_multiply"></a>

#### do\_multiply

```python
def do_multiply(frame: Frame, args: list) -> int
```

Multiplies two evaluated values: a * b.

**Arguments**:

- `frame` _Frame_ - The current execution frame.
- `args` _list_ - A list containing two integers to multiply. Each integer can be a direct value or an expression that requires evaluation.


**Returns**:

- `int` - The result of multiplying the two evaluated values.

<a id="lgl_interpreter.do_divide"></a>

#### do\_divide

```python
def do_divide(frame: Frame, args: list) -> float
```

Divides two evaluated values: a / b.

**Arguments**:

- `frame` _Frame_ - The current execution frame.
- `args` _list_ - A list containing two integers to divide. Each integer can be a direct value or an expression that requires evaluation.


**Returns**:

- `float` - The result of dividing the numerator by the denominator.


**Raises**:

- `AssertionError` - If the denominator is zero.

<a id="lgl_interpreter.do_power"></a>

#### do\_power

```python
def do_power(frame: Frame, args: list) -> int
```

Computes the result of raising a base to a specified exponent: base^(exponent).

**Arguments**:

- `frame` _Frame_ - The current execution frame.
- `args` _list_ - A list containing two integers to compute the power. Each integer can be a direct value or an expression that requires evaluation.


**Returns**:

- `int` - The result of base raised to the power of the exponent.

<a id="lgl_interpreter.do_AND"></a>

#### do\_AND

```python
def do_AND(frame: Frame, args: list) -> int
```

Performs the AND boolean operation: a AND b.

**Examples**:

  1 AND 1 = 1
  1 AND 0 = 0
  0 AND 1 = 0
  0 AND 0 = 0


**Arguments**:

- `frame` _Frame_ - The current execution frame.
- `args` _list_ - A list containing two boolean values (0 or 1). Each value can be a direct 0 or 1 or an expression that requires evaluation.


**Returns**:

- `int` - The result of the boolean operation a AND b.

<a id="lgl_interpreter.do_OR"></a>

#### do\_OR

```python
def do_OR(frame: Frame, args: list) -> int
```

Performs the OR boolean operation: a OR b.

**Examples**:

  1 OR 1 = 1
  1 OR 0 = 1
  0 OR 1 = 1
  0 OR 0 = 0


**Arguments**:

- `frame` _Frame_ - The current execution frame.
- `args` _list_ - A list containing two boolean values (0 or 1). Each value can be a direct 0 or 1 or an expression that requires evaluation.


**Returns**:

- `int` - The result of the boolean operation a OR b.

<a id="lgl_interpreter.do_XOR"></a>

#### do\_XOR

```python
def do_XOR(frame: Frame, args: list) -> int
```

Performs the XOR boolean operation: a XOR b.

**Examples**:

  1 XOR 1 = 0
  1 XOR 0 = 1
  0 XOR 1 = 1
  0 XOR 0 = 0


**Arguments**:

- `frame` _Frame_ - The current execution frame.
- `args` _list_ - A list containing two boolean values (0 or 1). Each value can be a direct 0 or 1 or an expression that requires evaluation.


**Returns**:

- `int` - The result of the boolean operation a XOR b.

<a id="lgl_interpreter.do_seq"></a>

#### do\_seq

```python
def do_seq(frame: Frame, args: list) -> any
```

Evaluates a sequence of expressions in order and returns the result of the last expression.

**Arguments**:

- `frame` _Frame_ - The current execution frame.
- `args` _list_ - A list of expressions to evaluate sequentially.


**Returns**:

- `any` - The result of the last evaluated expression.

<a id="lgl_interpreter.do_function"></a>

#### do\_function

```python
def do_function(frame: Frame, args: list) -> Function
```

Creates a new Function object with specified parameters and body.

**Arguments**:

- `frame` _Frame_ - The current execution frame.
- `args` _list_ - A list containing the parameters and body of the function.


**Returns**:

- `Function` - A Function object with its parameters and body.

<a id="lgl_interpreter.do_set"></a>

#### do\_set

```python
def do_set(frame: Frame, args: list) -> None
```

Sets a new variable in the current frame. If the value is not atomic, it will be evaluated before being set.

**Arguments**:

- `frame` _Frame_ - The current execution frame in which the variable will be set.
- `args` _list_ - A list containing the variable name and its value. The value will be evaluated if it requires further computation.


**Returns**:

  None

<a id="lgl_interpreter.do_get"></a>

#### do\_get

```python
def do_get(frame: Frame, args: list) -> any
```

Retrieves the value of a specified variable from the current or parent frames.

**Arguments**:

- `frame` _Frame_ - The current execution frame.
- `args` _list_ - A list containing the name of the variable.


**Returns**:

- `any` - The value of the variable.

<a id="lgl_interpreter.do_call"></a>

#### do\_call

```python
@Trace.decorate
def do_call(frame: Frame, args: list) -> any
```

Calls the specified function with provided arguments. If the arguments are not atomic, they will be evaluated before calling the function.

**Arguments**:

- `frame` _Frame_ - The current execution frame.
- `args` _list_ - A list containing the function name and parameters.


**Returns**:

- `any` - The result of the function call.

<a id="lgl_interpreter.do"></a>

#### do

```python
def do(frame: Frame, args: list) -> any
```

Evaluates the specified list of expressions.

**Arguments**:

- `frame` _Frame_ - The current execution frame.
- `args` _list_ - A list containing the operation name, either as a prefix (first element) or an infix (second element), followed by the expression.


**Returns**:

- `any` - The result of the evaluated expression (or 'None' for 'set').

<a id="lgl_interpreter.operations"></a>

#### operations

```python
def operations(operation_name: str) -> callable
```

Matches the operation from the LGL code to the actual method by searching for it in the global frame.

**Arguments**:

- `operation_name` _str_ - The name of the operation.


**Returns**:

- `callable` - The function corresponding to the operation name.


**Raises**:

- `KeyError` - If the operation name does not correspond to a valid function.

<a id="lgl_interpreter.load_lgl"></a>

#### load\_lgl

```python
def load_lgl(file_name: str) -> list
```

Loads the LGL code (list of expressions) from a file.

**Arguments**:

- `file_name` _str_ - The path to the file containing the LGL code (.gsc file).


**Returns**:

- `list` - The LGL code as a list.

<a id="lgl_interpreter.main"></a>

#### main

```python
def main() -> None
```

Main entry point for the LGL interpreter. Parses command-line arguments, loads the LGL code,
executes it, and optionally writes a trace log if specified.

## Reporting Documentation

#### parse\_log

```python
def parse_log(log_file: str) -> dict
```

Parses a log file generated by the 'Trace.write' from 'lgl_interpreter' to extract function call data. Sort the rows of the .csv (excluding the header) according to the function ID and then iterate through each call pair recording the function call amount and the total time spent on each function type (identified by name).

**Arguments**:

- `log_file` _str_ - Path to the log file containing function call events.


**Returns**:

- `dict` - A dictionary with the function name as key and another dictionary a the value containing the number of calls and the total time as keys.

<a id="reporting.print_results"></a>

#### print\_results

```python
def print_results(data: dict) -> None
```

Prints formatted function call statistics, including the name, the number of calls, total time,
and average time per function.

**Arguments**:

- `data` _dict_ - A dictionary with function call data parsed from the log file by 'parse_log'.

<a id="reporting.main"></a>

#### main

```python
def main() -> None
```

Main entry point for reporting. Expects a log file as a command-line argument
and outputs formatted function statistics to the console.