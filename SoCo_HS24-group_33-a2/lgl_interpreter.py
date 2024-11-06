from datetime import datetime
from hashlib import sha256
import csv
import time


class Frame:
    """
    This class imitates real Python frames (environments).
    Allows for nested function definitions.
    """

    def __init__(self, parent: "Frame" = None) -> None:
        self.parent = parent
        self.environment = {}

    def get(self, var_name: str) -> any:
        """
        Look for the variable with given name the current frame.
        If not found, recursively look at parents.

        Args:
            var_name (str): The name of the to-be found variable

        Returns:
            any: The value of the found variable

        Raises:
            KeyError: If the variable was not found
        """
        if var_name in self.environment:
            return self.environment[var_name]
        elif self.parent:
            return self.parent.get(var_name)
        else:
            raise KeyError(f"{var_name} was not found.")

    def add(self, name: str, value: any) -> None:
        """
        Add a new variable with given name and value to the current frame.

        Args:
            name (str): The name of the variable
            value (any): The value of the variable

        Return:
            None: Returns nothing
        """
        self.environment[name] = value


class Function:
    """
    This class imitates Python functions
    Implements callability for functions defined in lgl
    """

    def __init__(self, parameters: str | list[str], body: list) -> None:
        self.parameters = parameters if isinstance(parameters, list) else [parameters]
        self.body = body

    def call(self, current_frame: Frame, evaluated_args: list[int]) -> any:
        """
        Calls this Function object
        Creates a new frame for the function, assigns the provided arguments to its parameters, and then evaluates the function body

        Args:
            evaluated_args (list[int]): A list of evaluated arguments to pass to the function parameters

        Return:
            any: The result of evaluating the function's body
        """
        new_frame = Frame(current_frame)
        for parameter, arg in zip(self.parameters, evaluated_args):
            new_frame.add(parameter, arg)
        return do(new_frame, self.body)


class Trace:
    """
    This class holds every functionality of tracing the call stack. Provides a decorator '@Trace.decorate' that, when set, logs the call stack.
    """

    call_stack = []

    def __init__(self, function_name: str) -> None:
        self.id: str = self.__hash(function_name)
        self.function_name = function_name

    @staticmethod
    def decorate(func: callable) -> any:
        """
        Wrap any function containing the '@Trace.decorate' decorator. Add an entry to the call stack whenever a function starts and stops executing.

        Args:
            func (callable): The wrapped function to execute

        Returns:
            any: Returns the return value of the wrapped function
        """

        def inner(*args) -> any:
            function_name = args[1][0]
            trace = Trace(function_name)
            trace.add("start")
            result = func(*args)
            trace.add("stop")
            return result

        return inner

    @classmethod
    def write(cls, file_path: str) -> None:
        """
        Log the call stack to a .csv file.

        Args:
            file_path (str): The path to log the call stack to

        Returns:
            None: Returns nothing
        """
        with open(file_path, "w", newline="") as file:
            header = [["id", "timestamp", "function_name", "event"]]
            writer = csv.writer(file)
            writer.writerows(header + cls.call_stack)

    def add(self, event: str) -> None:
        """
        Add an event to the call stack.

        Args:
            event (str): The event, e.g. 'start', 'stop'

        Returns:
            None: Returns nothing
        """
        Trace.call_stack.append([self.id, self.__accurate_clock(), self.function_name, event])

    def __hash(self, function_name: str) -> str:
        """
        Generate a hash out of a function name and the current date and time to create a unique six digit hash.

        Args:
            function_name (str): The name of the function to be used as hashing parameter

        Returns:
            str: The string representation of the first six digits of the hash
        """
        data = f"{function_name}{self.__accurate_clock()}"
        return sha256(data.encode()).hexdigest()[:6]

    def __accurate_clock(self) -> str:
        """
        Get the accurate time (only 'datetime.now()' yielded same timing)
        """
        datetime_part = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        perf_counter_part = int((time.perf_counter() % 1) * 1000000)
        return f"{datetime_part}.{perf_counter_part:06d}"


def do_add(frame: Frame, args: list) -> int:
    """
    Adds two evaluated values: a + b

    Args:
        frame (Frame): The current execution frame
        args (list): A list containing two integers to add. Each integer can be a direct value or an expression that requires evaluation

    Returns:
        int: The resulting value of adding two evaluated values
    """
    assert len(args) == 2
    a = do(frame, args[0]) if isinstance(args[0], list) else args[0]
    b = do(frame, args[1]) if isinstance(args[1], list) else args[1]
    return a + b


def do_subtract(frame: Frame, args: list) -> int:
    """
    Substracts two evaluated values: a - b

    Args:
        frame (Frame): The current execution frame
        args (list): A list containing two integers to substract. Each integer can be a direct value or an expression that requires evaluation

    Returns:
        int: The resulting value of substracting two evaluated values
    """
    assert len(args) == 2
    a = do(frame, args[0]) if isinstance(args[0], list) else args[0]
    b = do(frame, args[1]) if isinstance(args[1], list) else args[1]
    return a - b


def do_multiply(frame: Frame, args: list) -> int:
    """
    Multiplies two evaluated values: a * b

    Args:
        frame (Frame): The current execution frame
        args (list): A list containing two integers to multiply. Each integer can be a direct value or an expression that requires evaluation

    Returns:
        int: The resulting value of multiplying two evaluated values
    """
    assert len(args) == 2
    a = do(frame, args[0]) if isinstance(args[0], list) else args[0]
    b = do(frame, args[1]) if isinstance(args[1], list) else args[1]
    return a * b


def do_divide(frame: Frame, args: list) -> float:
    """
    Divides two evaluated values: a / b

    Args:
        frame (Frame): The current execution frame
        args (list): A list containing two integers to divide. Each integer can be a direct value or an expression that requires evaluation

    Returns:
        float: The resulting value of dividing the numerator by the denominator
    """
    assert len(args) == 2
    numerator = do(frame, args[0]) if isinstance(args[0], list) else args[0]
    denominator = do(frame, args[1]) if isinstance(args[1], list) else args[1]
    assert denominator != 0, "Invalid division: denominator is 0"
    return round(numerator / denominator, 2)


def do_power(frame: Frame, args: list) -> int:
    """
    Computes the result of raising a base to a specified exponent: base^(exponent)

    Args:
        frame (Frame): The current execution frame
        args (list): A list containing two integers to compute the power. Each integer can be a direct value or an expression that requires evaluation.

    Returns:
        int: The result of base raised to the power of exponent
    """
    assert len(args) == 2
    base = do(frame, args[0]) if isinstance(args[0], list) else args[0]
    exponent = do(frame, args[1]) if isinstance(args[1], list) else args[1]
    return base**exponent


def do_AND(frame: Frame, args: list) -> int:
    """
    AND boolean operation: a AND b

    1 AND 1 = 1
    1 AND 0 = 0
    0 AND 1 = 0
    0 AND 0 = 0

    Args:
        frame (Frame): The current execution frame
        args (list): A list containing two boolean values (0 or 1). Each boolean value (0 or 1) can be a direct 0 or 1 or an expression that requires evaluation

    Returns:
        int: The result of the boolean operation a AND b
    """
    assert len(args) == 2
    a = do(frame, args[0]) if isinstance(args[0], list) else args[0]
    b = do(frame, args[1]) if isinstance(args[1], list) else args[1]
    a = 1 if a != 0 else 0
    b = 1 if b != 0 else 0
    return a & b


def do_OR(frame: Frame, args: list) -> int:
    """
    OR boolean operation: a OR b

    1 OR 1 = 1
    1 OR 0 = 1
    0 OR 1 = 1
    0 OR 0 = 0

    Args:
        frame (Frame): The current execution frame
        args (list): A list containing two boolean values (0 or 1). Each boolean value (0 or 1) can be a direct 0 or 1 or an expression that requires evaluation

    Returns:
        int: The result of the boolean operation a OR b
    """
    assert len(args) == 2
    a = do(frame, args[0]) if isinstance(args[0], list) else args[0]
    b = do(frame, args[1]) if isinstance(args[1], list) else args[1]
    a = 1 if a != 0 else 0
    b = 1 if b != 0 else 0
    return a | b


def do_XOR(frame: Frame, args: list) -> int:
    """
    XOR boolean operation: a XOR b

    1 XOR 1 = 0
    1 XOR 0 = 1
    0 XOR 1 = 1
    0 XOR 0 = 0

    Args:
        frame (Frame): The current execution frame
        args (list): A list containing two boolean values (0 or 1). Each boolean value (0 or 1) can be a direct 0 or 1 or an expression that requires evaluation

    Returns:
        int: The result of the boolean operation a XOR b
    """
    assert len(args) == 2
    a = do(frame, args[0]) if isinstance(args[0], list) else args[0]
    b = do(frame, args[1]) if isinstance(args[1], list) else args[1]
    a = 1 if a != 0 else 0
    b = 1 if b != 0 else 0
    return a ^ b


def do_seq(frame: Frame, args: list) -> any:
    """
    Evaluates a sequence of expression in order and returns the result of the last expression

    Args:
        frame (Frame): The current execution frame
        args (list): A list expressions to evaluate sequentially

    Returns:
        any: The result of the last evaluated expression
    """
    assert len(args) > 1
    for expr in args:
        evaluated_expr = do(frame, expr)
    return evaluated_expr


def do_function(_: Frame, args: list) -> Function:
    """
    Creates a new Function object with its parameter(s) and body

    Args:
        _ (Frame): The current execution frame
        args (list): A list containing the parameters and the body of the function

    Returns:
        Function: Function object with its parameter(s) and body
    """
    assert len(args) == 2
    parameters = args[0]
    body = args[1]
    return Function(parameters, body)


def do_set(frame: Frame, args: list) -> None:
    """
    Sets a new variable to the current frame
    If the value is not a atomic value, it will be evaluated before being set

    Args:
        frame (Frame): The current execution frame in which the new variable will be set
        args (list): A list containing the new variable name and its value. Value will be evaluated if it is an expression that needs evaluation

    Returns:
        None: Returns nothing
    """
    assert len(args) == 2
    name = args[0]
    value = do(frame, args[1]) if isinstance(args[1], list) else args[1]
    frame.add(name, value)


def do_get(frame: Frame, args: list) -> any:
    """
    Retrieves the specified variable's value from the current frame or any parent frame if not found.

    Args:
        frame (Frame): The current execution frame
        args(list): A list containing the name of the variable

    Returns:
        any: The value of the variable
    """
    assert len(args) == 1
    variable_name = args[0]
    return frame.get(variable_name)


@Trace.decorate
def do_call(frame: Frame, args: list) -> any:
    """
    Calls the passed function with the given arguments

    Args:
        frame (Frame): The current execution frame
        args(list): A list containing the function name and the parameter(s)

    Returns
        any: The output of the called function
    """
    function_name = args[0]
    arguments = [do(frame, arg) if isinstance(arg, list) else arg for arg in args[1:]]
    func = frame.get(function_name)
    return func.call(frame, arguments)


def do(frame: Frame, args: list) -> any:
    """
    Evaluates the given expression

    Args:
        frame (Frame): The current execution frame.
        args (list): A list containing the operation name, either as a prefix (first element) or an infix (second element), followed by the expression

    Return:
        any: The result of the evaluated expression (except 'None' for 'set')
    """

    if args[1] in ["+", "-", "*", "/", "^", "AND", "OR", "XOR"]:
        operation_name = ""
        match args[1]:
            case "+":
                operation_name = "add"
            case "-":
                operation_name = "subtract"
            case "*":
                operation_name = "multiply"
            case "/":
                operation_name = "divide"
            case "^":
                operation_name = "power"
            case "AND":
                operation_name = "AND"
            case "OR":
                operation_name = "OR"
            case "XOR":
                operation_name = "XOR"
        args = [operation_name, args[0], args[2]]

    operation_name = args[0]
    arguments = args[1:]
    return operations(operation_name)(frame, arguments)


def operations(operation_name: str) -> callable:
    modified_name = "do_" + operation_name
    if modified_name in globals():
        return globals()[modified_name]
    raise KeyError(f"{operation_name} was not found.")


def load_lgl(file_name: str) -> list:
    """
    Load the LGL code

    Args:
        file_name (str): The path to the file containing the LGL code (.gsc file)

    Returns
        list: The LGL code as a list
    """
    import json

    with open(file_name, "r") as file:
        return json.load(file)


def main() -> None:
    import argparse

    arg_parser = argparse.ArgumentParser(description="LGL interpreter")
    arg_parser.add_argument("filename", type=str, help="Path to file containing LGL code (.gsc file)")
    arg_parser.add_argument("--trace", type=str, help="Path to store trace log")
    args = arg_parser.parse_args()

    global_frame = Frame()
    program = load_lgl(args.filename)
    result = do(global_frame, program)
    print(result)

    if args.trace:
        Trace.write(args.trace)


if __name__ == "__main__":
    main()
