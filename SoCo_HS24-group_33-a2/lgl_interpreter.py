from datetime import datetime
from hashlib import sha256
import csv


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
    This class imitates Python functions.
    Implements callability for functions defined in lgl.
    """

    def __init__(self, frame: Frame, parameters: str | list[str], body: list) -> None:
        self.__frame = frame
        self.parameters = parameters
        self.body = body

    def call(self, *parsed_args: tuple[int]) -> any:
        """
        Call this function.
        Add passed arguments to the current frame and then call 'parse' to resolve the values (i.e. execute the function).

        Args:
            parsed_args (tuple of int): Arguments passed to the to-be called function

        Return:
            any: Return the result of calling the function
        """
        new_frame = Frame(self.__frame)
        for parameter, arg in zip(self.parameters, parsed_args):
            new_frame.add(parameter, arg)
        return parse(new_frame, self.body)


class Trace:

    call_stack = []
    file_path = None

    def __init__(self, function_name: str) -> None:
        self.id: str = self.__hash(function_name)
        self.function_name = function_name

    def start(self) -> None:
        self.__add(f"{datetime.now()}", "start")

    def stop(self) -> None:
        self.__add(f"{datetime.now()}", "stop")

    def write(cls, file_path: str) -> None:
        if not file_path is None:
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(cls.call_stack)
        else:
            raise ValueError(
                "Logging path has not been set yet. Set it with Trace.set_file_path()!"
            )

    def __add(self, timestamp: str, event: str) -> None:
        Trace.call_stack.append([self.id, timestamp, self.function_name, event])

    def __hash(self, function_name: str):
        data = f"{function_name}{datetime.now()}"
        return sha256(data.encode()).hexdigest()[:6]


def trace(func):
    def inner(*args) -> any:
        tr = Trace(args[1])
        tr.start()
        result = func(*args)
        tr.stop()
        return result

    return inner


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
    Sets a new variable to the current frame.
    If the value is not a atomic value, it will be evaluated before being set.

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
        frame (Frame): The current execution frame.
        args(list): A list containing the name of the variable

    Returns:
        any: The value of the variable
    """
    assert len(args) == 1
    variable_name = args[0]
    return frame.get(variable_name)


def do_call(frame: Frame, args: list) -> any:
    """
    Calls the passed function with the given arguments

    Args:
        frame (Frame): The current execution frame.
        args(list): A list containing the function name and the parameter(s)

    Returns
        any: The output of the called function
    """
    function_name = args[0]
    arguments = [do(frame, arg) if isinstance(arg, list) else arg for arg in args[1:]]
    func = frame.get(function_name)
    return func.call(frame, arguments)


def sanitize_expression(expression: list[any]) -> tuple[any, any, any]:
    """
    Return the third item of the expression in the correct format: Return 'None' if the third element does not exist, a value if the third item is a single value and a list if the expression contains more than three items.

    Args:
        expression (list of any): Expression to be sanitized and split

    Return:
        tuple of any: Split and sanitized expression
    """
    id_0 = expression[0]
    id_1 = expression[1]
    id_2 = None
    if len(expression) == 3:
        id_2 = expression[2]
    elif len(expression) > 3:
        id_2 = expression[2:]
    return id_0, id_1, id_2


def parse(frame: Frame, expression: list) -> any:
    """
    Parse content between two brackets [] and find correct method to call.

    Args:
        frame (Frame): The frame to read/write from
        expression (list): lgl expression

    Return:
        any: The single atomic value (except 'None' for 'set')

    Raises:
        ValueError: If the expression contains invalid identifiers
    """
    valid_identifier_id_0 = [
        "seq",
        "set",
        "get",
        "call",
        "function",
        "add",
        "subtract",
        "multiply",
        "divide",
        "power",
    ]
    valid_identifier_id_1 = ["+", "-", "*", "/", "^"]
    id_0, id_1, id_2 = sanitize_expression(expression)
    if isinstance(id_0, str) and id_0 in valid_identifier_id_0:
        match id_0:
            case "seq":
                return seq(frame, expression)
            case "set":
                return set(frame, id_1, id_2)
            case "get":
                return get(frame, id_1)
            case "call":
                return call(frame, id_1, id_2)
            case "function":
                return function(frame, id_1, id_2)
            case "add":
                return add(id_1, id_2)
            case "subtract":
                return subtract(id_1, id_2)
            case "multiply":
                return multiply(id_1, id_2)
            case "divide":
                return divide(id_1, id_2)
            case "power":
                return power(id_1, id_2)
    elif isinstance(id_1, str) and id_1 in valid_identifier_id_1:
        id_0 = parse(frame, id_0) if isinstance(id_0, list) else id_0
        id_2 = parse(frame, id_2) if isinstance(id_2, list) else id_2
        match id_1:
            case "+":
                return add(id_0, id_2)
            case "-":
                return subtract(id_0, id_2)
            case "*":
                return multiply(id_0, id_2)
            case "/":
                return divide(id_0, id_2)
            case "^":
                return power(id_0, id_2)
            case "AND":
                return AND(id_0, id_2)
            case "OR":
                return OR(id_0, id_2)
            case "XOR":
                return XOR(id_0, id_2)
    raise ValueError(f"{id_0} or {id_1} are not valid identifiers.")


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


def trace(file_name: str) -> any:
    pass


def main() -> None:
    import argparse

    arg_parser = argparse.ArgumentParser(description="LGL interpreter")
    arg_parser.add_argument(
        "filename", type=str, help="Path to file containing LGL code (.gsc file)"
    )
    arg_parser.add_argument("--trace", type=str, help="Path to store trace log")
    args = arg_parser.parse_args()

    global_frame = Frame()
    program = load_lgl(args.filename)
    result = parse(global_frame, program)
    print(result)

    if args.trace:
        Trace.write(args.trace)


if __name__ == "__main__":
    main()
