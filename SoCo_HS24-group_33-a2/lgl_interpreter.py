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

    def call(self, *args) -> None:
        pass


def add(frame: Frame, a: int | list, b: int | list) -> int:
    assert not isinstance(a,list) or len(a) == 3
    assert not isinstance(b,list) or len(b) == 3

    left = parse(frame,a) if isinstance(a,list) else a
    right = parse(frame,b) if isinstance(b,list) else b

    return right + left

def subtract(frame: Frame, a: int | list, b: int | list) -> int:
    assert not isinstance(a,list) or len(a) == 3
    assert not isinstance(b,list) or len(b) == 3

    left = parse(frame,a) if isinstance(a,list) else a
    right = parse(frame,b) if isinstance(b,list) else b

    return left - right


def multiply(frame: Frame, a: int | list, b: int | list) -> int:
    pass


def divide(frame: Frame, numerator: int | list, denominator: int | list) -> int:
    pass


def power(frame: Frame, base: int | list, exponent: int | list) -> int:
    pass


def AND(frame: Frame, a: int | list, b: int | list) -> int:
    pass


def OR(frame: Frame, a: int | list, b: int | list) -> int:
    pass


def XOR(frame: Frame, a: int | list, b: int | list) -> int:
    pass


def parse(frame: Frame, expression: list) -> any:
    """
    Parse content between two brackets [] and find correct method to call.
    The called methods (e.g. 'add') are responsible to resolve nesting.

    Example: [[2, "+", 2], "+", 3]
    'parse' calls 'add' with parameters [2, "+", 2] and 3. 'add' can't simply compute it because the first parameter is a list. But it is 'add's responsibilty to call 'parse' again with the parameter [2, "+", 2], so that it receives an actual value back which then can be used to add 3 to it.
    """
    valid_identifier_id_0 = ["set", "get", "call", "function"]
    valid_identifier_id_1 = ["+", "-", "*", "/"]
    id_0 = expression[0]
    id_1 = expression[1]
    id_2 = expression[2:] if len(expression) > 2 else None
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
                return add(id_0, id_2)
            case "-":
                return subtract(id_0, id_2)
            case "*":
                return multiply(id_0, id_2)
            case "/":
                return divide(id_0, id_2)
            case "AND":
                return AND(id_0, id_2)
            case "OR":
                return OR(id_0, id_2)
            case "XOR":
                return XOR(id_0, id_2)
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
    pass


def get(frame: Frame, name: str) -> any:
    """
    Retrieve a variable of the current frame (or parents if not found)
    """
    pass


def call(frame: Frame, name: str, args: list) -> None:
    """
    Retrieve the function of the current frame (or parents if not found) and call it
    """
    pass


def main() -> None:
    """
    Entry point to setup global frame and then call parse()
    """