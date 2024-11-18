class Commit:
    """
    Class that can be instanciated to represent one single commit but also serves all other functionalities that have to do with committing.
    """

    def __init__(self, date: str, message: str, records: list[tuple[str, str]]) -> None:
        def __unique_id() -> str:
            """
            Generate a unique ID to identify the commit.
            """
            pass

        self.__id = __unique_id()
        self.__date = date
        self.__message = message
        self.__manifest = records

    @staticmethod
    def commit(message: str) -> None:
        """
        Add a new commit_xxx.json file containing the commit ID (unique), commit date and commit message along with all previously staged records. Remove the newly commited files from the 'staged.json' file. Add the timestamp in the filename. Copy the files to the backup.
        """
        pass

    @staticmethod
    def all() -> list["Commit"]:
        """
        Return all commits (oldest first, newest last)
        """

        def __read() -> "Commit":
            """Convert a commit_xxx.json file to a 'Commit' object"""
            pass

    @staticmethod
    def latest() -> "Commit":
        """
        Return the most recent commit.
        """
        return Commit.all()[-1]

    def id(self) -> str:
        """
        Return the unique ID of the commit.
        """
        pass

    def manifest(self) -> list[tuple[str, str]]:
        """
        Get all records in this commit as a tuple of (filename, hash)
        """
        pass

    def files(self) -> list[str]:
        """
        Get all file names in this commit as a string.
        """

    def write(self) -> "Commit":
        """Write a commit_xxx.json file containing the current variables."""
        pass

    def __str__(self) -> str:
        """
        String representation of this object. Used when printing via Print(some_commit).
        """
        return f"[{self.id} | {self.date} | {self.message}]"  # TO-DO: Make prettier
