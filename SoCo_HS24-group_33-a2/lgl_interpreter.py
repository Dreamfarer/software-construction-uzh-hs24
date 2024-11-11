from datetime import datetime
from hashlib import sha256
import csv
import time


class Frame:
    """
    Mimics real Python frames (environments), enabling nested function definitions.
    """

    def __init__(self, parent: "Frame" = None) -> None:
        """
        Initializes a new frame with an optional parent frame.

        Args:
            parent (Frame, optional): The parent frame. Defaults to None.
        """
        self.parent = parent
        self.environment = {}

    def get(self, var_name: str) -> any:
        """
        Retrieves the value of a variable with the given name from the current frame.
        If not found, searches recursively in parent frames.

        Args:
            var_name (str): The name of the variable to find.

        Returns:
            any: The value of the found variable.

        Raises:
            KeyError: If the variable is not found in the current or any parent frame.
        """
        if var_name in self.environment:
            return self.environment[var_name]
        elif self.parent:
            return self.parent.get(var_name)
        else:
            raise KeyError(f"{var_name} was not found.")

    def add(self, name: str, value: any) -> None:
        """
        Adds a new variable with the given name and value to the current frame.

        Args:
            name (str): The name of the variable.
            value (any): The value of the variable.

        Returns:
            None
        """
        self.environment[name] = value


class Function:
    """
    Imitates a Python function. This class holds the function's parameters, body, and frame, which contains variables and other functions defined within this function. It also implements the callability of the 'Function' object.
    """

    def __init__(self, parameters: str | list[str], body: list, frame: Frame) -> None:
        """
        Initializes a Function instance with parameters, body, and a frame.

        Args:
            parameters (str | list[str]): The parameters of the function
            body (list): The body of the function, represented as a list of expressions.
            frame (Frame): The frame in which the function's variables and nested functions are defined.
        """
        self.parameters = parameters if isinstance(parameters, list) else [parameters]
        self.body = body
        self.frame = Frame(frame)

    def call(self, evaluated_args: list[int]) -> any:
        """
        Calls this 'Function' object. Adds the parameters as variables to the current frame and evaluates the function body in the current frame.

        Args:
            evaluated_args (list[int]): A list of evaluated expressions to assign to the function parameters.

        Returns:
            any: The result of evaluating the function's body.
        """
        for parameter, arg in zip(self.parameters, evaluated_args):
            self.frame.add(parameter, arg)
        return do(self.frame, self.body)


class Trace:
    """
    Handles functionality for tracing the call stack. Provides a decorator '@Trace.decorate' 
    that logs entries to the call stack when functions start and stop execution.
    """

    call_stack = []

    def __init__(self, function_name: str) -> None:
        """
        Initializes a Trace instance with a unique ID and the function name.

        Args:
            function_name (str): The name of the function being traced.
        """
        self.id: str = self.__hash(function_name)
        self.function_name = function_name

    @staticmethod
    def decorate(func: callable) -> callable:
        """
        Decorator to wrap functions with trace logging. Adds an entry to the call stack 
        whenever the decorated function starts and stops executing.

        Args:
            func (callable): The function to be wrapped and traced.

        Returns:
            callable: The wrapped function with trace logging.
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
        Logs the call stack to a specified .csv file.

        Args:
            file_path (str): The file path where the call stack should be logged.

        Returns:
            None
        """
        with open(file_path, "w", newline="") as file:
            header = [["id", "timestamp", "function_name", "event"]]
            writer = csv.writer(file)
            writer.writerows(header + cls.call_stack)

    def add(self, event: str) -> None:
        """
        Adds an event to the call stack.

        Args:
            event (str): The event type, such as 'start' or 'stop'.

        Returns:
            None
        """
        Trace.call_stack.append(
            [self.id, self.__accurate_clock(), self.function_name, event]
        )

    def __hash(self, function_name: str) -> str:
        """
        Generates a unique six digit hash for a function based on its name and the current timestamp.

        Args:
            function_name (str): The function name to be used in generating the hash.

        Returns:
            str: A string representation of the first six characters of the hash.
        """
        data = f"{function_name}{self.__accurate_clock()}"
        return sha256(data.encode()).hexdigest()[:6]

    def __accurate_clock(self) -> str:
        """
        Provides an accurate timestamp combining 'datetime' and 'perf_counter'.

        Returns:
            str: A timestamp with high precision, formatted as 'YYYY-MM-DD HH:MM:SS.microseconds'.
        """
        datetime_part = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        perf_counter_part = int((time.perf_counter() % 1) * 1000000)
        return f"{datetime_part}.{perf_counter_part:06d}"


def do_add(frame: Frame, args: list) -> int:
    """
    Adds two evaluated values: a + b.

    Args:
        frame (Frame): The current execution frame.
        args (list): A list containing two integers to add. Each integer can be a direct value or an expression that requires evaluation.

    Returns:
        int: The result of adding the two evaluated values.
    """
    assert len(args) == 2
    a = do(frame, args[0]) if isinstance(args[0], list) else args[0]
    b = do(frame, args[1]) if isinstance(args[1], list) else args[1]
    return a + b


def do_subtract(frame: Frame, args: list) -> int:
    """
    Subtracts two evaluated values: a - b.

    Args:
        frame (Frame): The current execution frame.
        args (list): A list containing two integers to subtract. Each integer can be a direct value or an expression that requires evaluation.

    Returns:
        int: The result of subtracting the two evaluated values.
    """
    assert len(args) == 2
    a = do(frame, args[0]) if isinstance(args[0], list) else args[0]
    b = do(frame, args[1]) if isinstance(args[1], list) else args[1]
    return a - b


def do_multiply(frame: Frame, args: list) -> int:
    """
    Multiplies two evaluated values: a * b.

    Args:
        frame (Frame): The current execution frame.
        args (list): A list containing two integers to multiply. Each integer can be a direct value or an expression that requires evaluation.

    Returns:
        int: The result of multiplying the two evaluated values.
    """
    assert len(args) == 2
    a = do(frame, args[0]) if isinstance(args[0], list) else args[0]
    b = do(frame, args[1]) if isinstance(args[1], list) else args[1]
    return a * b


def do_divide(frame: Frame, args: list) -> float:
    """
    Divides two evaluated values: a / b.

    Args:
        frame (Frame): The current execution frame.
        args (list): A list containing two integers to divide. Each integer can be a direct value or an expression that requires evaluation.

    Returns:
        float: The result of dividing the numerator by the denominator.

    Raises:
        AssertionError: If the denominator is zero.
    """
    assert len(args) == 2
    numerator = do(frame, args[0]) if isinstance(args[0], list) else args[0]
    denominator = do(frame, args[1]) if isinstance(args[1], list) else args[1]
    assert denominator != 0, "Invalid division: denominator is 0"
    return round(numerator / denominator, 2)


def do_power(frame: Frame, args: list) -> int:
    """
    Computes the result of raising a base to a specified exponent: base^(exponent).

    Args:
        frame (Frame): The current execution frame.
        args (list): A list containing two integers to compute the power. Each integer can be a direct value or an expression that requires evaluation.

    Returns:
        int: The result of base raised to the power of the exponent.
    """
    assert len(args) == 2
    base = do(frame, args[0]) if isinstance(args[0], list) else args[0]
    exponent = do(frame, args[1]) if isinstance(args[1], list) else args[1]
    return base**exponent


def do_AND(frame: Frame, args: list) -> int:
    """
    Performs the AND boolean operation: a AND b.

    Examples:
        1 AND 1 = 1
        1 AND 0 = 0
        0 AND 1 = 0
        0 AND 0 = 0

    Args:
        frame (Frame): The current execution frame.
        args (list): A list containing two boolean values (0 or 1). Each value can be a direct 0 or 1 or an expression that requires evaluation.

    Returns:
        int: The result of the boolean operation a AND b.
    """
    assert len(args) == 2
    a = do(frame, args[0]) if isinstance(args[0], list) else args[0]
    b = do(frame, args[1]) if isinstance(args[1], list) else args[1]
    a = 1 if a != 0 else 0
    b = 1 if b != 0 else 0
    return a & b


def do_OR(frame: Frame, args: list) -> int:
    """
    Performs the OR boolean operation: a OR b.

    Examples:
        1 OR 1 = 1
        1 OR 0 = 1
        0 OR 1 = 1
        0 OR 0 = 0

    Args:
        frame (Frame): The current execution frame.
        args (list): A list containing two boolean values (0 or 1). Each value can be a direct 0 or 1 or an expression that requires evaluation.

    Returns:
        int: The result of the boolean operation a OR b.
    """
    assert len(args) == 2
    a = do(frame, args[0]) if isinstance(args[0], list) else args[0]
    b = do(frame, args[1]) if isinstance(args[1], list) else args[1]
    a = 1 if a != 0 else 0
    b = 1 if b != 0 else 0
    return a | b


def do_XOR(frame: Frame, args: list) -> int:
    """
    Performs the XOR boolean operation: a XOR b.

    Examples:
        1 XOR 1 = 0
        1 XOR 0 = 1
        0 XOR 1 = 1
        0 XOR 0 = 0

    Args:
        frame (Frame): The current execution frame.
        args (list): A list containing two boolean values (0 or 1). Each value can be a direct 0 or 1 or an expression that requires evaluation.

    Returns:
        int: The result of the boolean operation a XOR b.
    """
    assert len(args) == 2
    a = do(frame, args[0]) if isinstance(args[0], list) else args[0]
    b = do(frame, args[1]) if isinstance(args[1], list) else args[1]
    a = 1 if a != 0 else 0
    b = 1 if b != 0 else 0
    return a ^ b


def do_seq(frame: Frame, args: list) -> any:
    """
    Evaluates a sequence of expressions in order and returns the result of the last expression.

    Args:
        frame (Frame): The current execution frame.
        args (list): A list of expressions to evaluate sequentially.

    Returns:
        any: The result of the last evaluated expression.
    """
    assert len(args) > 1
    for expr in args:
        evaluated_expr = do(frame, expr)
    return evaluated_expr


def do_function(frame: Frame, args: list) -> Function:
    """
    Creates a new Function object with specified parameters and body.

    Args:
        frame (Frame): The current execution frame.
        args (list): A list containing the parameters and body of the function.

    Returns:
        Function: A Function object with its parameters and body.
    """
    assert len(args) == 2
    parameters = args[0]
    body = args[1]
    return Function(parameters, body, frame)


def do_set(frame: Frame, args: list) -> None:
    """
    Sets a new variable in the current frame. If the value is not atomic, it will be evaluated before being set.

    Args:
        frame (Frame): The current execution frame in which the variable will be set.
        args (list): A list containing the variable name and its value. The value will be evaluated if it requires further computation.

    Returns:
        None
    """
    assert len(args) == 2
    name = args[0]
    value = do(frame, args[1]) if isinstance(args[1], list) else args[1]
    frame.add(name, value)


def do_get(frame: Frame, args: list) -> any:
    """
    Retrieves the value of a specified variable from the current or parent frames.

    Args:
        frame (Frame): The current execution frame.
        args (list): A list containing the name of the variable.

    Returns:
        any: The value of the variable.
    """
    assert len(args) == 1
    variable_name = args[0]
    return frame.get(variable_name)


@Trace.decorate
def do_call(frame: Frame, args: list) -> any:
    """
    Calls the specified function with provided arguments. If the arguments are not atomic, they will be evaluated before calling the function.

    Args:
        frame (Frame): The current execution frame.
        args (list): A list containing the function name and parameters.

    Returns:
        any: The result of the function call.
    """
    function_name = args[0]
    arguments = [do(frame, arg) if isinstance(arg, list) else arg for arg in args[1:]]
    func = frame.get(function_name)
    return func.call(arguments)


def do(frame: Frame, args: list) -> any:
    """
    Evaluates the specified list of expressions.

    Args:
        frame (Frame): The current execution frame.
        args (list): A list containing the operation name, either as a prefix (first element) or an infix (second element), followed by the expression.

    Returns:
        any: The result of the evaluated expression (or 'None' for 'set').
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
    """
    Matches the operation from the LGL code to the actual method by searching for it in the global frame.

    Args:
        operation_name (str): The name of the operation.

    Returns:
        callable: The function corresponding to the operation name.

    Raises:
        KeyError: If the operation name does not correspond to a valid function.
    """
    modified_name = "do_" + operation_name
    if modified_name in globals():
        return globals()[modified_name]
    raise KeyError(f"{operation_name} was not found.")


def load_lgl(file_name: str) -> list:
    """
    Loads the LGL code (list of expressions) from a file.

    Args:
        file_name (str): The path to the file containing the LGL code (.gsc file).

    Returns:
        list: The LGL code as a list.
    """
    import json

    with open(file_name, "r") as file:
        return json.load(file)


def main() -> None:
    """
    Main entry point for the LGL interpreter. Parses command-line arguments, loads the LGL code,
    executes it, and optionally writes a trace log if specified.
    """
    import argparse

    arg_parser = argparse.ArgumentParser(description="LGL interpreter")
    arg_parser.add_argument(
        "filename", type=str, help="Path to file containing LGL code (.gsc file)"
    )
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
