class Frame:
    """
    This class imitates real Python frames (environments). Allows for nested function definitions.
    """

    def __init__(self, parent: "Frame" = None) -> None:
        self.parent = parent
        self.environment = {}
        self.content = []

    def get(self, var_name: str) -> any:
        """Look in the current frame. If not found, recursively look at parents."""
        if not var_name in self.environment:
            if self.parent == None:
                raise KeyError(f"{var_name} was not found.")
            return self.parent.get(var_name)
        return self.environment[var_name]

    def add(self, name: str, value: any) -> None:
        """Add to the current frame"""
        self.environment[name] = value


def add(a: int, b: int) -> int:
    pass


def subtract(a: int, b: int) -> int:
    pass


def multiply(a: int, b: int) -> int:
    pass


def divide(numerator: int, denominator: int) -> int:
    pass


def power(base: int, exponent: int) -> int:
    pass


def parse(frame: Frame, expression: list) -> any:
    """
    Parse content between two brackets [] and find correct method to call.
    """
    identifier = expression[0]
    name = expression[1]
    value = expression[2:] if len(expression) > 2 else None
    match identifier:
        case "set":
            return set(frame, name, value)
        case "get":
            return get(frame, name)
        case "call":
            return call(frame, name, value)
        case _:
            raise ValueError(f"{identifier} is not a valid identifier.")


def function(frame: Frame, parameter: list[str] | str, body: list) -> callable:
    """
    Introduce a new function
    Create a new frame along with every function introduction
    If the body or the parameters cannot be set right away (e.g. because of nesting or evaluation), call 'parse' again on the part that cannot be resolved right away (divide-and-conquer).
    """
    pass


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
