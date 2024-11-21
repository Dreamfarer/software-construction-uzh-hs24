import os
import json
from record import Record


class Status:

    STATUS_FILE = ".status.json"

    @staticmethod
    def untracked() -> list[Record]:
        """
        Return a list of untracked records.
        """
        return [r for r in Status.__read_json() if r.status == Record.UNTRACKED]

    @staticmethod
    def modified() -> list[Record]:
        """
        Return a list of modified records.
        """
        return [r for r in Status.__read_json() if r.status == Record.MODIFIED]

    @staticmethod
    def staged() -> list[Record]:
        """
        Return a list of staged records.
        """
        return [r for r in Status.__read_json() if r.status == Record.STAGED]

    @staticmethod
    def commited() -> list[Record]:
        """
        Return a list of committed records.
        """
        return [r for r in Status.__read_json() if r.status == Record.COMMITED]

    @staticmethod
    def add(record: Record) -> None:
        """
        Add a new record to the '.status.json' file.
        If the record already exists (same filename and hash), it won't be added.
        """
        records = Status.__read_json()
        if not any(r.filename == record.filename and r.hash == record.hash for r in records):
            records.append(record)
            Status.__write_json(records)

    @staticmethod
    def remove(record: Record) -> None:
        """
        Remove a specific record from the '.status.json' file.
        Identifies the record by matching the filename and hash.
        """
        records = Status.__read_json()
        records = [r for r in records if not (r.filename == record.filename and r.hash == record.hash)]
        Status.__write_json(records)

    @staticmethod
    def move(record: Record, status: int) -> None:
        """
        Move a record into another status (e.g. go from staged to commited)
        """
        record.status = status
        Status.remove(record)
        Status.add(record)

    @staticmethod
    def status() -> None:
        """
        Print the current status of each file in the working directory, indicating if they are untracked, modified, staged, or committed.
        """
        pass

    @staticmethod
    def __read_json() -> list[Record]:
        """
        Return the current records from the '.status.json' file.
        Return an empty list, if the file is currently empty.
        """
        if os.path.exists(Status.STATUS_FILE):
            with open(Status.STATUS_FILE, "r") as file:
                records = []
                for r in json.load(file):
                    records.append(Record(r["filename"], r["status"], r["hash"]))
                return records
        return []

    @staticmethod
    def __write_json(records: list[Record]) -> None:
        """
        Write the records to the '.status.json' file.
        """
        with open(Status.STATUS_FILE, "w") as file:
            json.dump([r.to_dict() for r in records], file, indent=4)
