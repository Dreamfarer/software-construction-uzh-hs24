import os


class Record:

    UNTRACKED = 0
    MODIFIED = 1
    STAGED = 2
    COMMITED = 3

    def __init__(self, filename: str, status: int, hash: str = None) -> None:
        self.filename = filename
        self.status = status
        self.hash = hash if not hash is None else Record.get_hash(filename)

    def to_dict(self) -> dict:
        """
        Convert the Record object to a dictionary.
        """
        return {"filename": self.filename, "hash": self.hash, "status": self.status}

    @staticmethod
    def to_dicts(records: list["Record"]):
        """
        Covert a list of Records to a list of ditionaries.
        """
        return [r.to_dict() for r in records]

    @staticmethod
    def get_hash(filename: str) -> str:
        """
        Get the SHA-1 hash of a specific file in the current working directory by reading 4 KB per read operation.
        """
        import hashlib

        absolute_path = os.path.abspath(filename)
        sha1 = hashlib.sha1()
        with open(absolute_path, "rb") as file:
            while chunk := file.read(4096):
                sha1.update(chunk)
        return sha1.hexdigest()
