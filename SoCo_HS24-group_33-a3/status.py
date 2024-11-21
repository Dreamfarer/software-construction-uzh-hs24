import os
import json
from record import Record


class Status:

    STATUS_FILE = os.path.join(".tig", ".status.json")

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
    def all() -> list[Record]:
        """
        Return a list of all records.
        """
        return Status.__read_json()

    @staticmethod
    def add(record: Record) -> None:
        """
        Add a new record to the '.status.json' file.
        If the record already exists (same filename and hash), it won't be added.
        If a record with the same filename but a different status exists, update its status.
        """
        records = Status.__read_json()
        for r in records:
            if r.filename == record.filename and r.hash == record.hash:
                if r.status != record.status:
                    r.status = record.status
                break
        else:
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
        Move a record into another status (e.g., go from staged to committed).
        """
        records = Status.__read_json()
        for r in records:
            if r.filename == record.filename and r.hash == record.hash:
                r.status = status  # Update status in-place
                break
        else:
            # If the record doesn't exist, add it with the new status
            record.status = status
            records.append(record)
        Status.__write_json(records)

    # To-Do: Make prettier
    @staticmethod
    def status() -> None:
        """
        Print the current status of each file in the working directory, indicating if they are untracked, modified, staged, or committed.
        """
        for record in Status.__read_json():
            print(f"Filename: {record.filename} | Status: {record.status} | Hash: {record.hash}")

    @staticmethod
    def sync() -> None:
        """
        Synchronize the current files in the working directory with the .status.json file.
        If the filename or hash of a file has changed, call move() and update its status to Record.MODIFIED.
        """
        current_records = Status.all()
        current_files = Status.__records()
        filename_lookup = {record.filename: record for record in current_records}
        for file_record in current_files:
            existing_record = filename_lookup.get(file_record.filename)
            if existing_record:
                if existing_record.hash != file_record.hash:
                    Status.move(existing_record, Record.MODIFIED)
            else:
                Status.add(file_record)
        current_file_names = {file_record.filename for file_record in current_files}
        for record in current_records:
            if record.filename not in current_file_names:
                Status.remove(record)

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

    @staticmethod
    def __records() -> list[Record]:
        """
        Get the records of each file in the current working directory as a Record instance.
        Each record is initalized with the status UNTRACKED, as all other files are already present in the '.status.json'
        """

        records = []
        for root, dirs, filenames in os.walk("."):
            dirs[:] = [d for d in dirs if d not in (".tig")]
            for filename in filenames:
                relative_path = os.path.relpath(os.path.join(root, filename), start=".")
                records.append(Record(relative_path, 0))
        return records
