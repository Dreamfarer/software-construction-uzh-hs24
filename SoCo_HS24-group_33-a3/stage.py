from record import Record
from status import Status


class Stage:
    """
    Class that cannot be instanciated. Only serves all functionality related to staging.
    """

    @staticmethod
    def add(filename: str) -> None:
        """
        Add the provided file to the '.status.json' file if it has not already been staged before.
        """
        Status.add(Record(filename, Record.STAGED))
