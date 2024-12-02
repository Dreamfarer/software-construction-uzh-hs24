from record import Record
from status import Status


class Stage:
    """
    Handles the `add` command by instructing `Status` to mark files for inclusion in the next commit.
    """

    @staticmethod
    def add(filename: str) -> None:
        """
        Instructing 'Status' to add the file to the '.status.json' staging area.

        Args:
            filename (str): The name of the file to be staged.

        Returns:
            None
        """
        Status.add(Record(filename, Record.STAGED))
