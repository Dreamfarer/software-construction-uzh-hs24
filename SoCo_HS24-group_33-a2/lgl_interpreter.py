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


def add(a: int, b: int) -> int:
    """
    Add two values: a + b

    Args:
        a (int): Value a
        b (int): Value b

    Returns:
        int: The resulting value of adding two values
    """
    return a + b


def subtract(a: int, b: int) -> int:
    """
    Subtract two values: a - b

    Args:
        a (int): Value a
        b (int): Value b

    Returns:
        int: The resulting value of subtracting b from a
    """
    return a - b


def multiply(a: int, b: int) -> int:
    """
    Multiply two values: a * b

    Args:
        a (int): Value a
        b (int): Value b

    Returns:
        int: The resulting value of multiplying a and b
    """
    return a * b


def divide(numerator: int, denominator: int) -> int:
    """
    Divides to values and rounds the value to two decimal places: numerator / denominator

    Args:
        numerator (int): Numerator
        denominator (int): Denominator

    Returns:
        int: The resulting value of dividing the numerator by the denominator
    """
    assert denominator != 0, "Invalid division: denominator is 0"
    return round(numerator / denominator, 2)


def power(base: int, exponent: int) -> int:
    """
    Computes the result of raising a base to a specified exponent: base^(exponent)

    Args:
        base (int): Base
        exponent (int): Exponent

    Returns:
        int: The result of base raised to the power of exponent.
    """
    return base**exponent


def AND(a: int, b: int) -> int:
    """
    AND boolean operation: a AND b

    1 AND 1 = 1
    1 AND 0 = 0
    0 AND 1 = 0
    0 AND 0 = 0

    Args:
        a (int): boolean a
        b (int): boolean b

    Returns:
        int: The result of the boolean operation a AND b
    """
    a = 1 if a != 0 else 0
    b = 1 if b != 0 else 0
    return a & b


def OR(a: int, b: int) -> int:
    """
    AND boolean operation: a OR b

    1 OR 1 = 1
    1 OR 0 = 1
    0 OR 1 = 1
    0 OR 0 = 0

    Args:
        a (int): Boolean a
        b (int): Boolean b

    Returns:
        int: The result of the boolean operation a OR b
    """
    a = 1 if a != 0 else 0
    b = 1 if b != 0 else 0
    return a | b


def XOR(a: int, b: int) -> int:
    """
    XOR boolean operation: a XOR b

    1 XOR 1 = 0
    1 XOR 0 = 1
    0 XOR 1 = 1
    0 XOR 0 = 0

    Args:
        a (int): Boolean a
        b (int): Boolean b

    Returns:
        int: The result of the boolean operation a XOR b
    """
    a = 1 if a != 0 else 0
    b = 1 if b != 0 else 0
    return a ^ b


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
    valid_identifier_id_0 = ["set", "get", "call", "function"]
    valid_identifier_id_1 = ["+", "-", "*", "/", "^"]
    id_0, id_1, id_2 = sanitize_expression(expression)
    if isinstance(id_0, str) and id_0 in valid_identifier_id_0:
        match id_0:
            case "set":
                return set(frame, id_1, id_2)
            case "get":
                return get(frame, id_1)
            case "call":
                return call(frame, id_1, id_2)
            case "function":
                return function(frame, id_1, id_2)
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


def function(frame: Frame, parameters: list[str] | str, body: list) -> Function:
    """
    Add new function to provided Frame (only initialization)
    Create a new frame along with every function introduction.

    Args:
        frame (Frame): The frame to add the function to
        parameters (list of str): The parameter of said function in lgl
        body (list): The body of said function in lgl
    """
    function_frame = Frame(frame.parent)
    return Function(function_frame, parameters, body)


def set(frame: Frame, name: str, value: int | list) -> None:
    """
    Set a new variable to the current frame.
    If the value cannot be set right away (e.g. because of non atomic value), call 'parse' again on the part that cannot be resolved right away (divide-and-conquer).

    Args:
        frame (Frame): The frame to set the new variable to
        name (str): The name of said variable
        value (list | int): The value of said variable

    Returns:
        None: Returns nothing
    """
    if isinstance(value, list):
        value = parse(frame, value)
    frame.add(name, value)


def get(frame: Frame, name: str) -> any:
    """
    Retrieve a variable of the current frame (or parents if not found).

    Args:
        frame (Frame): The frame to get the variable from
        name (str): The name of the variable

    Returns:
        any: The value of the variable

    """
    return frame.get(name)


def call(frame: Frame, name: str, args: list) -> any:
    """
    Retrieve the function of the current frame (or parents if not found) and call it.

    Args:
        frame (Frame): The frame to call the function from
        name (str): The name of the function to call
        args (list): The arguments to call said function with

    Returns
        any: The output of the called function
    """
    func = frame.get(name)
    if not isinstance(func, Function):
        raise ValueError(f"'{name}' is not a function")
    parsed_args = [parse(frame, arg) if isinstance(arg, list) else arg for arg in args]
    return func.call(*parsed_args)


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
        trace(args.trace)


if __name__ == "__main__":
    main()
