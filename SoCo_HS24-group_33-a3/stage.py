import os
import json
from tig import TIG
from backup import Backup


class Stage:
    """
    Class that cannot be instanciated. Only serves all functionality related to staging.
    """

    STAGED_FILE = os.path.join(".stage", "staged.json")

    @staticmethod
    def add(filenames: str | list[str]) -> None:
        """
        Add the provided files to the 'staged.json' file containg all currently staged files if it has not already been staged before.
        """
        if isinstance(filenames, str):
            filenames = [filenames]
        staged_records = Stage.__read_json()
        existing_hashes = [record[1] for record in staged_records]
        for filename in filenames:
            record = TIG.record(filename)
            if not record[1] in existing_hashes:
                Backup.add(os.path.dirname(Stage.STAGED_FILE), record)
                staged_records.append(record)
        Stage.__write_json(staged_records)

    @staticmethod
    def remove(record: tuple[str, str]) -> None:
        """
        Remove provided files from the 'staged.json' file.
        """
        staged_records = Stage.__read_json()
        print(record)
        staged_records.remove(record)
        Stage.__write_json(staged_records)

    @staticmethod
    def manifest() -> list[tuple[str, str]]:
        """
        Return a list of the records that are currently staged (return the 'staged.json' file content).
        """
        return Stage.__read_json()

    @staticmethod
    def __read_json() -> list[tuple[str, str]]:
        """
        Return the current records from the 'staged.json' file.
        Return an empty list, if the file is currently empty.
        """
        os.makedirs(os.path.dirname(Stage.STAGED_FILE), exist_ok=True)
        if os.path.exists(Stage.STAGED_FILE):
            with open(Stage.STAGED_FILE, "r") as file:
                return [tuple(record) for record in json.load(file)]
        return []

    @staticmethod
    def __write_json(staged_records: list[tuple[str, str]]) -> None:
        """
        Write the current records to the '.staged/staged.json' file.
        """
        os.makedirs(os.path.dirname(Stage.STAGED_FILE), exist_ok=True)
        with open(Stage.STAGED_FILE, "w") as file:
            json.dump([list(record) for record in staged_records], file, indent=4)
