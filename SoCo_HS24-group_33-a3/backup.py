import os
import shutil
from record import Record
from status import Status


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
        from commit import Commit

        commit = None
        for c in Commit.all():
            if c._id == id:
                commit = c
                break
        if commit == None:
            print(f"No commit found with ID: {id}")
            return

        restored_files = []
        for record in commit.manifest():
            _, file_extension = os.path.splitext(record.filename)
            source_path = os.path.join(".tig", "backup", record.hash + file_extension)
            destination_path = os.path.join(os.getcwd(), record.filename)
            restored_files.append(destination_path)
            shutil.copy(source_path, destination_path)

        for root, _, files in os.walk(os.getcwd()):
            untracked_files = [os.path.join(root, r.filename) for r in Status.untracked()]
            if root.startswith(os.path.join(os.getcwd(), ".tig")):
                continue
            for file in files:
                file_path = os.path.join(root, file)
                if file_path not in restored_files and file_path not in untracked_files:
                    os.remove(file_path)
