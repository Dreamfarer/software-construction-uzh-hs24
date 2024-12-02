from hashlib import sha256
from datetime import datetime
from record import Record
from status import Status
from backup import Backup
import json
import os

YELLOW = "\033[33m"
RESET = "\033[0m"


class Commit:
    """
    Processes the `commit` command, creates commit files, and uses `Backup` to archive files. It also provides access to commit history for other commands.
    """

    def __init__(self, date: str, message: str, records: list[Record], commit_id: str = None) -> None:
        """
        Initializes a Commit instance.

        Args:
            date (str): The date of the commit.
            message (str): The commit message.
            records (list[Record]): The records associated with this commit.
            commit_id (str, optional): The unique identifier for the commit. Defaults to None.

        Returns:
            None
        """
        self._date = date
        self._message = message
        self._manifest = records
        self._id = commit_id if commit_id else self.__unique_id()

    @staticmethod
    def commit(message: str) -> None:
        """
        Creates a new commit and instructs a status chanage and the creation of a backup for the files in the commit.

        Args:
            message (str): The commit message.

        Returns:
            None
        """
        staged_files = Status.staged()
        if not staged_files:
            print("No changes to commit.")
            return
        commit_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_commit = Commit(commit_date, message, staged_files)
        for record in staged_files:
            Status.move(record, record.hash, Record.COMMITED)
        new_commit.write()
        Backup.add(".tig/backup", staged_files)

    @staticmethod
    def all() -> list["Commit"]:
        """
        Retrieves all commits in chronological order.

        Returns:
            list[Commit]: A list of all commits, sorted from oldest to newest.
        """

        def __read(file_path: str) -> "Commit":
            """
            Converts a commit_xxx.json file to a Commit object.

            Args:
                file_path (str): The path to the commit JSON file.

            Returns:
                Commit: The Commit object created from the JSON file.
            """
            with open(file_path, "r") as commit_file:
                json_dict = json.load(commit_file)
                records = [Record(**record) for record in json_dict["records"]]
                return Commit(
                    date=json_dict["date"],
                    message=json_dict["message"],
                    records=records,
                    commit_id=json_dict["commit_id"],
                )

        commit_folder = ".tig/commits"
        if not os.path.exists(commit_folder):
            return []
        commit_files = sorted(
            [os.path.join(commit_folder, fname) for fname in os.listdir(commit_folder) if fname.startswith("commit_")]
        )
        return [__read(c) for c in commit_files]

    @staticmethod
    def latest() -> "Commit":
        """
        Retrieves the most recent commit.

        Returns:
            Commit: The latest commit.
        """
        return Commit.all()[-1]

    def id(self) -> str:
        """
        Retrieves the unique identifier for this commit.

        Returns:
            str: The commit ID.
        """
        return self._id

    def manifest(self) -> list[Record]:
        """
        Retrieves all records associated with this commit.

        Returns:
            list[Record]: A list of records associated with this commit.
        """
        return self._manifest

    def files(self) -> list[str]:
        """
        Retrieves all file names from the records associated with this commit.

        Returns:
            list[str]: A list of names of all files present in the records associated with this commit.
        """
        return [r[0] for r in self._manifest]

    def write(self) -> "Commit":
        """
        Writes the commit information to a JSON file. Creates a file named commit_xxx.json containing the commit ID, date, message, and records.

        Returns:
            Commit: The commit itself.
        """
        commit_filename = f".tig/commits/commit_{self._id}_{self._date.replace(' ','_').replace(':','-')}.json"
        os.makedirs(os.path.dirname(commit_filename), exist_ok=True)
        commit_data = {
            "commit_id": self._id,
            "date": self._date,
            "message": self._message,
            "records": Record.to_dicts(self._manifest),
        }
        with open(commit_filename, "w") as commit_file:
            json.dump(commit_data, commit_file, indent=4)

    def __unique_id(self) -> str:
        """
        Generates a unique identifier for the commit based on its message and date.

        Returns:
            str: A unique hash-based identifier for the commit.
        """
        data = self._message + self._date
        hash_code = sha256(data.encode()).hexdigest()
        return hash_code[:8]

    def __str__(self) -> str:
        """
        Returns a string representation of the this commit.

        Returns:
            str: A formatted string containing the commit ID, date, and message of this commit.
        """
        return f"{YELLOW}commit {self._id}{RESET}\nDate: {self._date}\n\n   {self._message}\n"
