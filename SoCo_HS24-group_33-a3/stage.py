import os
import json
from tig import TIG


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
                staged_records.append(record)
        Stage.__write_json(staged_records)

    @staticmethod
    def remove(filenames: str | list[str]) -> None:
        """
        Remove provided files from the 'staged.json' file.
        """
        pass

    @staticmethod
    def manifest() -> list[tuple[str, str]]:
        """
        Return a list of the records that are currently staged (return the 'staged.json' file content).
        """
        pass

    @staticmethod
    def __read_json() -> list[tuple[int, int]]:
        """
        Return the current records from the 'staged.json' file.
        Return an empty list, if the file is currently empty.
        """
        os.makedirs(os.path.dirname(Stage.STAGED_FILE), exist_ok=True)
        if os.path.exists(Stage.STAGED_FILE):
            with open(Stage.STAGED_FILE, "r") as file:
                return json.load(file)
        return []

    @staticmethod
    def __write_json(staged_records: list[tuple[int, int]]) -> None:
        """
        Write the current records to the '.staged/staged.json' file.
        """
        os.makedirs(os.path.dirname(Stage.STAGED_FILE), exist_ok=True)
        with open(Stage.STAGED_FILE, "w") as file:
            json.dump(staged_records, file, indent=4)


Stage.add("test3.txt")
