class TIG:
    """
    Class that holds all functionality which is tig general or simply does not belong to committing and staging.
    """

    @staticmethod
    def init(dir: str) -> None:
        """Create a new '.tig/' folder inside the provided path."""
        import os

        path = os.path.join(dir, ".tig")
        if not os.path.exists(path):
            os.mkdir(path)

    @staticmethod
    def status() -> None:
        """
        Print the current status of each file in the working directory, indicating if they are untracked, modified,staged, or committed.
        Use 'get_untracked_files()', 'get_modified_files()', 'get_staged_files()', 'get_commited_files()'.
        """
        pass

    @staticmethod
    def log(number: int = 5) -> None:
        """
        Print the commit ID, commit date, and commit message of the last N commits. If -N is not given, the default N=5 is used.
        Essentially pretty print the string representation of each commit of 'Commit.all()'
        """
        pass

    @staticmethod
    def diff(filename: str) -> None:
        """
        Compare the current version of the file with its last committed version. Print the differences in a unified diff format. Use a library for this.
        """
        pass

    @staticmethod
    def records() -> list[tuple[str, str]]:
        """
        Get the records of each file in the current working directory as a tuple of (filename, hash)
        """
        import os
        import hashlib

        def hash(path: str) -> str:
            """
            Calculate the SHA-1 hash from the file content by reading 4 KB per read operation.
            """
            sha1 = hashlib.sha1()
            with open(path, "rb") as file:
                while chunk := file.read(4096):
                    sha1.update(chunk)
            return sha1.hexdigest()

        records = []
        for root, dirs, filenames in os.walk("."):
            dirs[:] = [d for d in dirs if d not in (".stage", ".commit")]
            for filename in filenames:
                path = os.path.join(root, filename)
                relative_path = os.path.relpath(path, start=".")
                file_hash = hash(path)
                records.append((relative_path, file_hash))
        return records

    @staticmethod
    def get_untracked_files() -> list[str]:
        """Return the list of files that are not staged (get with Stage.current()) and are also not commited (get with Commit.latest().files())"""
        pass

    @staticmethod
    def get_modified_files() -> list[str]:
        """
        Return a list of files that have a different record than in the latest commit. Use 'TIG.records()' to get all records and 'Commit.latest().manifest()' to get the records of the latest commit.
        """
        pass


if __name__ == "__main__":
    from parser import Parser

    Parser.parse()
