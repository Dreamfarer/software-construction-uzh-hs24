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
        If the record already exists (same filename or same hash), merely modify it without adding.
        """
        records = Status.__read_json()
        for i, r in enumerate(records):
            if r.filename == record.filename or r.hash == record.hash:
                records[i] = record
                return Status.__write_json(records)
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
    def move(record: Record, hash: str, status: int) -> None:
        """
        Move a record into another status (e.g., go from staged to committed).
        """
        records = Status.__read_json()
        for r in records:
            if r.filename == record.filename and r.hash == record.hash:
                r.status = status
                r.hash = hash
                break
        else:
            record.status = status
            records.append(record)
        Status.__write_json(records)

    @staticmethod
    def status() -> None:
        """
        Print the current status of each file in the working directory, indicating if they are untracked, modified, staged, or committed.
        """
        records = Status.__read_json()
        max_filename_length = max(len(record.filename) for record in records)
        max_status_length = max(len(Record.REPRESENT[record.status]) for record in records)
        max_hash_length = max(len(record.hash) for record in records)
        print(
            f"{'Filename'.ljust(max_filename_length)} | {'Status'.ljust(max_status_length)} | {'Hash'.ljust(max_hash_length)}"
        )
        print("-" * (max_filename_length + max_status_length + max_hash_length + 6))
        for record in records:
            print(
                f"{record.filename.ljust(max_filename_length)} | {Record.REPRESENT[record.status].ljust(max_status_length)} | {record.hash.ljust(max_hash_length)}"
            )

    @staticmethod
    def sync() -> None:
        """
        Synchronize the current files in the working directory with the .status.json file.
        If the filename or hash of a file has changed, update its status accordingly.
        """
        current_records = Status.all()
        current_files = Status.__records()
        filename_lookup = {record.filename: record for record in current_records}
        hash_lookup = {record.hash: record for record in current_records}
        for file_record in current_files:
            existing_record = filename_lookup.get(file_record.filename)
            if existing_record:
                if existing_record.hash != file_record.hash:
                    Status.move(existing_record, file_record.hash, Record.MODIFIED)
            else:
                existing_by_hash = hash_lookup.get(file_record.hash)
                if existing_by_hash:
                    Status.move(existing_by_hash, file_record.hash, Record.MODIFIED)
                else:
                    Status.add(file_record)
        current_file_names = {file_record.filename for file_record in current_files}
        for record in current_records:
            if record.filename not in current_file_names:
                if record.hash not in {file_record.hash for file_record in current_files}:
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
