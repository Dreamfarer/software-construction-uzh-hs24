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
    Class that can be instanciated to represent one single commit but also serves all other functionalities that have to do with committing.
    """

    def __init__(self, date: str, message: str, records: list[Record], commit_id: str = None) -> None:

        self._date = date
        self._message = message
        self._manifest = records
        self._id = commit_id if commit_id else self.__unique_id()

    @staticmethod
    def commit(message: str) -> None:
        """
        Add a new commit_xxx.json file containing the commit ID (unique), commit date and commit message along with all previously staged records.
        Move the staged files to commited files '.status.json'.
        Add the timestamp in the filename. Copy the files to the backup.
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
        Return all commits (oldest first, newest last)
        """

        def __read(file_path) -> "Commit":
            """Convert a commit_xxx.json file to a 'Commit' object"""
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
        Return the most recent commit.
        """
        return Commit.all()[-1]

    def id(self) -> str:
        """
        Return the unique ID of the commit.
        """
        return self._id

    def manifest(self) -> list[Record]:
        """
        Get all records in this commit.
        """
        return self._manifest

    def files(self) -> list[str]:
        """
        Get all file names in this commit as a string.
        """
        return [r[0] for r in self._manifest]

    def write(self) -> "Commit":
        """
        Write a commit_xxx.json file containing the current variables.
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
        Generate a unique ID to identify the commit.
        """
        data = self._message + self._date
        hash_code = sha256(data.encode()).hexdigest()
        return hash_code[:8]

    def __str__(self) -> str:
        """
        String representation of this object. Used when printing via Print(some_commit).
        """
        return f"{YELLOW}commit {self._id}{RESET}\nDate: {self._date}\n\n   {self._message}\n"
