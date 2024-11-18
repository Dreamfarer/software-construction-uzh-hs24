import os
import shutil


class Backup:
    """
    Class that handles all the backup-ing; moving, deleting files and so on.
    """

    @staticmethod
    def add(directory: str, records: str | list[str]) -> None:
        """
        Add a backup of the provided files (as record) to the provided directory.
        """
        if isinstance(records, tuple):
            records = [records]
        os.makedirs(directory, exist_ok=True)
        print(directory, records)
        for record in records:
            source_path = record[0]
            hash = record[1]
            _, file_extension = os.path.splitext(source_path)
            new_filename = hash + file_extension
            destination_path = os.path.join(directory, new_filename)
            shutil.copy(source_path, destination_path)

    @staticmethod
    def checkout(id: str) -> None:
        """
        Restore the directory's files to the state of a specific commit ID. Use the 'Commit' class to get the files you need to move.
        """
        pass
