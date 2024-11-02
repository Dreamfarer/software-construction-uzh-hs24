class Frame:
    """
    This class imitates real Python frames (environments). Allows for nested function definitions.
    """

    def __init__(self, parent: "Frame" = None) -> None:
        self.parent = parent
        self.environment = {}

    def get(self, var_name: str) -> any:
        """Look in the current frame. If not found, recursively look at parents."""
        if var_name in self.environment:
            return self.environment[var_name]
        elif self.parent:
            return self.parent.get(var_name)
        else:
            raise KeyError(f"{var_name} was not found.")

    def add(self, name: str, value: any) -> None:
        """Add to the current frame"""
        self.environment[name] = value


class Function:

    def __init__(self, frame: Frame, parameters: str | list[str], body: list) -> None:
        self.__frame = frame
        self.parameters = parameters
        self.body = body

    def call(self, *parsed_args) -> any:
        new_frame = Frame(self.__frame)
        for parameter, arg in zip(self.parameters, parsed_args):
            new_frame.add(parameter, arg)
        return parse(new_frame, self.body)


def add(frame: Frame, a: int | list, b: int | list) -> int:
    """
    Adds two values together.
    In terms of a list or nested list 'add' calls 'parse' recursively to resolve nesting.
    """
    assert not isinstance(a,list) or len(a) == 3
    assert not isinstance(b,list) or len(b) == 3

    left = parse(frame,a) if isinstance(a,list) else a
    right = parse(frame,b) if isinstance(b,list) else b

    return right + left

def subtract(frame: Frame, a: int | list, b: int | list) -> int:
    """
    Substract two values from each other.
    In terms of a list or nested list 'substract' calls 'parse' recursively to resolve nesting. 
    """
    assert not isinstance(a,list) or len(a) == 3
    assert not isinstance(b,list) or len(b) == 3

    left = parse(frame,a) if isinstance(a,list) else a
    right = parse(frame,b) if isinstance(b,list) else b

    return left - right


def multiply(frame: Frame, a: int | list, b: int | list) -> int:
    """
    Multiplies two values.
    In terms of a list or nested list 'multiply' calls 'parse' recursively to resolve nesting.
    """
    assert not isinstance(a,list) or len(a) == 3
    assert not isinstance(b,list) or len(b) == 3

    left = parse(frame,a) if isinstance(a,list) else a
    right = parse(frame,b) if isinstance(b,list) else b

    return left * right


def divide(frame: Frame, numerator: int | list, denominator: int | list) -> int:
    """
    Divides to values and rounds the value to two decimal places.
    In terms of a list or nested list 'divide' calls 'parse' recursively to resolve nesting.
    """
    assert not isinstance(numerator,list) or len(numerator) == 3
    assert not isinstance(denominator,list) or len(denominator) == 3

    numerator = parse(frame,numerator) if isinstance(numerator,list) else numerator
    denominator = parse(frame, denominator) if isinstance(denominator,list) else denominator

    assert denominator != 0, "Invalid division: denominator is 0"
    return round(numerator/denominator,2)

def power(frame: Frame, base: int | list, exponent: int | list) -> int:
    """
    Calculates the power of a given base with the corresponding exponent.
    In terms of a list or nested list 'power' calls 'parse' recursively to resolve nesting.
    """
    assert not isinstance(base, list) or len(base) == 3
    assert not isinstance(exponent,list) or len(exponent) == 3

    base = parse(frame, base) if isinstance(base,list) else base
    exponent = parse(frame,exponent) if isinstance(exponent,list) else exponent

    return base ** exponent


def AND(frame: Frame, a: int | list, b: int | list) -> int:
    """
    Implements the AND functionality:
    1 AND 1 = 1
    1 AND 0 = 0
    0 AND 1 = 0
    0 AND 0 = 0
    In terms of a list or nested list 'ADD' calls 'parse' recursively to resolve nesting.
    """
    assert not isinstance(a,list) or len(a) == 3
    assert not isinstance(b,list) or len(b) == 3

    left = parse(frame,a) if isinstance(a,list) else a
    right = parse(frame,b) if isinstance(b,list) else b

    left = 1 if left != 0 else 0
    right = 1 if right != 0 else 0

    return left & right


def OR(frame: Frame, a: int | list, b: int | list) -> int:
    """
    Implements the OR functionality:
    1 OR 1 = 1
    1 OR 0 = 1
    0 OR 1 = 1
    0 OR 0 = 0
    In terms of a list or nested list 'OR' calls 'parse' recursively to resolve nesting.
    """
    assert not isinstance(a,list) or len(a) == 3
    assert not isinstance(b,list) or len(b) == 3

    left = parse(frame,a) if isinstance(a,list) else a
    right = parse(frame,b) if isinstance(b,list) else b

    left = 1 if left != 0 else 0
    right = 1 if right != 0 else 0

    return left | right


def XOR(frame: Frame, a: int | list, b: int | list) -> int:
    """
    Implements the XOR functionality:
    1 XOR 1 = 0
    1 XOR 0 = 1
    0 XOR 1 = 1
    0 XOR 0 = 0
    In terms of a list or nested list 'XOR' calls 'parse' recursively to resolve nesting.
    """
    assert not isinstance(a,list) or len(a) == 3
    assert not isinstance(b,list) or len(b) == 3

    left = parse(frame,a) if isinstance(a,list) else a
    right = parse(frame,b) if isinstance(b,list) else b

    left = 1 if left != 0 else 0
    right = 1 if right != 0 else 0

    return left ^ right


def sanitize_expression(expression: list[any]) -> tuple[any, any, any]:
    """
    Return the third item of the expression in the correct format.
    Return 'None' if the third element does not exist, a value if the third item is a single value and a list if the expression contains more than three items.
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
    The called methods (e.g. 'add') are responsible to resolve nesting.

    Example: [[2, "+", 2], "+", 3]
    'parse' calls 'add' with parameters [2, "+", 2] and 3. 'add' can't simply compute it because the first parameter is a list. But it is 'add's responsibilty to call 'parse' again with the parameter [2, "+", 2], so that it receives an actual value back which then can be used to add 3 to it.
    """
    valid_identifier_id_0 = ["set", "get", "call", "function"]
    valid_identifier_id_1 = ["+", "-", "*", "/"]
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
        match id_1:
            case "+":
                return add(frame, id_0, id_2)
            case "-":
                return subtract(frame, id_0, id_2)
            case "*":
                return multiply(frame, id_0, id_2)
            case "/":
                return divide(frame, id_0, id_2)
            case "AND":
                return AND(frame, id_0, id_2)
            case "OR":
                return OR(frame, id_0, id_2)
            case "XOR":
                return XOR(frame, id_0, id_2)
    raise ValueError(f"{id_0} or {id_1} are not valid identifiers.")


def function(frame: Frame, parameters: list[str] | str, body: list) -> Function:
    """
    Introduce a new function
    Create a new frame along with every function introduction
    """
    function_frame = Frame(frame.parent)
    return Function(function_frame, parameters, body)


def set(frame: Frame, name: str, value: list) -> None:
    """
    Set a new variable to the current frame
    If the value cannot be set right away (e.g. because of evaluation), call 'parse' again on the part that cannot be resolved right away (divide-and-conquer).
    """
    if isinstance(value, list):
        value = parse(frame, value)
    frame.add(name, value)


def get(frame: Frame, name: str) -> any:
    """
    Retrieve a variable of the current frame (or parents if not found)
    """
    return frame.get(name)


def call(frame: Frame, name: str, args: list) -> any:
    """
    Retrieve the function of the current frame (or parents if not found) and call it
    """
    func = frame.get(name)
    if not isinstance(func, Function):
        raise ValueError(f"'{name}' is not a function")
    parsed_args = [parse(frame, arg) if isinstance(arg, list) else arg for arg in args]
    return func.call(*parsed_args)


def main() -> None:
    """
    Entry point to setup global frame and then call parse()
    """