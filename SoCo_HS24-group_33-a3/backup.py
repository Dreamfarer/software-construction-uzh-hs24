import os
import shutil


class Backup:
    """
    Class that handles all the backup-ing; moving, deleting files and so on.
    """

    @staticmethod
    def add(directory: str, records: tuple | list[tuple]) -> None:
        """
        Add a backup of the provided files (as record) to the provided directory.
        """
        if isinstance(records, tuple):
            records = [records]
        os.makedirs(directory, exist_ok=True)
        for record in records:
            source_path = record[0]
            hash = record[1]
            _, file_extension = os.path.splitext(source_path)
            new_filename = hash + file_extension
            destination_path = os.path.join(directory, new_filename)
            shutil.copy(source_path, destination_path)

    @staticmethod
    def remove(directory: str, records: tuple | list[tuple]) -> None:
        """
        Remove files with the specified hash names from the provided directory.
        """
        if isinstance(records, tuple):
            records = [records]
        for record in records:
            hash = record[1]
            for file in os.listdir(directory):
                if file.startswith(hash):
                    file_path = os.path.join(directory, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    break

    @staticmethod
    def checkout(id: str) -> None:
        """
        Restore the directory's files to the state of a specific commit ID. Use the 'Commit' class to get the files you need to move.
        """
        pass
