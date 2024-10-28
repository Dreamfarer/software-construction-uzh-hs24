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
    Recursively parse content between two brackets [] and find correct method to call.

    Example: ["set", "get_cube_power", ["function", "x", ["power", ["get", "x"], 3]]]
    The parser sees that ["function", "x", ["power", ["get", "x"], 3]] cannot directly
    be evaluated and therefore cannot be set right away, that's why it calls 'parse'
    again with this list.
    Then, in the recursive step, it calls 'function' to get a callable (which intern might
    also call 'parse' if something is not directly evaluatable). In the end,
    after returning from the recursive statements it adds "get_cube_power"
    as a callable to the current frame.
    """
    pass


def function(frame: Frame, parameter: list[str] | str, body: list) -> callable:
    """
    Introduce a new function
    Create a new frame along with every function introduction
    """
    pass


def set(frame: Frame, name: str, value: str | int | list) -> None:
    """
    Set a new variable to the current frame
    """
    pass


def get(frame: Frame, name: str) -> any:
    """
    Retrieve a variable of the current frame (or parents if not found)
    """
    pass


def call(frame: Frame, name: str, *args: any) -> None:
    """
    Retrieve the function of the current frame (or parents if not found) and call it
    """
    pass


def main() -> None:
    """
    Entry point to setup global frame and then call parse()
    """
