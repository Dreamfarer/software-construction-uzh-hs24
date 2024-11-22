import os
import shutil
from record import Record


class Backup:
    """
    Class that handles all the backup-ing; moving, deleting files and so on.
    """

    @staticmethod
    def add(directory: str, records: Record | list[Record]) -> None:
        """
        Add a backup of the provided files (as record) to the provided directory.
        """
        if not isinstance(records, list):
            records = [records]
        os.makedirs(directory, exist_ok=True)
        for record in records:
            _, file_extension = os.path.splitext(record.filename)
            new_filename = record.hash + file_extension
            destination_path = os.path.join(directory, new_filename)
            shutil.copy(record.filename, destination_path)

    @staticmethod
    def checkout(id: str) -> None:
        """
        Restore the directory's files to the state of a specific commit ID. Use the 'Commit' class to get the files you need to move.
        """
        pass
