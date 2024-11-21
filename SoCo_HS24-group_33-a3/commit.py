from hashlib import sha256
from datetime import datetime
from record import Record
from status import Status
from backup import Backup
import json

class Commit:
    """
    Class that can be instanciated to represent one single commit but also serves all other functionalities that have to do with committing.
    """

    def __init__(self, date: str, message: str, records: list[tuple[str, str]]) -> None:
        def __unique_id() -> str:
            """
            Generate a unique ID to identify the commit.
            """
            data = self.__message + self.__date
            hash_code = sha256(data).hexdigest()
            return hash_code

        self.__id = __unique_id()
        self.__date = date
        self.__message = message
        self.__manifest = records

    @staticmethod
    def commit(message: str) -> None:
        """
        Add a new commit_xxx.json file containing the commit ID (unique), commit date and commit message along with all previously staged records. Remove the newly commited files from the 'staged.json' file. Add the timestamp in the filename. Copy the files to the backup.
        """
        staged_files = Status.staged()
        commit_date  = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        commit = Commit(commit_date, message, staged_files)
        commit.write()

        Status.move(staged_files, Record.COMMITED)
        


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
        return self.__id

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
        commit_filename = f"commit_{self.__id}_{self.__date.replace(" ", "_").replace(":","-")}.json"
        commit_data = {
            "commit_id": self.__id,
            "date": self.__date,
            "message": self.__message,
            "records": self.__manifest
        }
        with open(commit_filename, "w") as commit_file:
            json.dump(commit_data, commit_file, indent=4)
        

    def __str__(self) -> str:
        """
        String representation of this object. Used when printing via Print(some_commit).
        """
        return f"[{self.id} | {self.date} | {self.message}]"  # TO-DO: Make prettier
