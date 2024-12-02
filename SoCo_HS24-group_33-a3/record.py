import os


class Record:
    """
    Represents entries in the repository's metadata files (e.g., commits and `.status.json`), holding attributes such as filenames, hashes, and statuses (untracked, modified, staged, or committed).
    """

    UNTRACKED = 0
    MODIFIED = 1
    STAGED = 2
    COMMITED = 3
    REPRESENT = {0: "untracked", 1: "modified", 2: "staged", 3: "commited"}

    def __init__(self, filename: str, status: int, hash: str = None) -> None:
        """
        Initializes a Record instance.

        Args:
            filename (str): The name of the file.
            status (int): The status of the file (e.g., untracked, modified).
            hash (str, optional): The hash of the file's content. Defaults to None.

        Returns:
            None
        """
        self.filename = filename
        self.status = status
        self.hash = hash if not hash is None else Record.get_hash(filename)

    def to_dict(self) -> dict:
        """
        Convert the this record to a dictionary.

        Returns:
            dict: A dictionary representation of this record.
        """
        return {"filename": self.filename, "hash": self.hash, "status": self.status}

    @staticmethod
    def to_dicts(records: list["Record"]):
        """
        Convert a list of records to a list of dictionaries.

        Args:
            records (list[Record]): A list of records.

        Returns:
            list[dict]: A list of dictionaries representing the records.
        """
        return [r.to_dict() for r in records]

    @staticmethod
    def get_hash(filename: str) -> str:
        """
        Get the SHA-1 hash of a specific file in the current working directory. Reads the file in chunks of 4 KB to compute the hash.

        Args:
            filename (str): The name of the file for which to compute the hash.

        Returns:
            str: The first 8 characters of the computed SHA-1 hash.
        """
        import hashlib

        absolute_path = os.path.abspath(filename)
        sha1 = hashlib.sha1()
        with open(absolute_path, "rb") as file:
            while chunk := file.read(4096):
                sha1.update(chunk)
        return sha1.hexdigest()[:8]
