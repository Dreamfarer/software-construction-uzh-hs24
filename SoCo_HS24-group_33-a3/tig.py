from commit import Commit
from status import Status
import os
from difflib import unified_diff


class TIG:
    """
    Handles lightweight commands like `init`, `log`, and `diff`. It initializes repositories, retrieves commit logs, and computes differences between file states. As the main entry point for Tig, it forwards commands to the `Parser`.
    """

    @staticmethod
    def init(dir: str) -> None:
        """
        Creates a new '.tig/' folder inside the provided path.

        Args:
            dir (str): The directory in which to create the '.tig/' folder.

        Returns:
            None
        """
        path = os.path.join(dir, ".tig")
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def log(number: int) -> None:
        """
        Prints the commit ID, commit date, and commit message of the last N commits. If `number` is not provided, defaults to N=5.

        Args:
            number (int): The number of recent commits to display.

        Returns:
            None
        """
        commits = sorted(Commit.all(), key=lambda commit: commit._date)
        for commit in commits[:-number]:
            print(f"commit {commit._id}")
            print(f"Date:   {commit._date}")
            print(f"\n    {commit._message}\n")

    @staticmethod
    def diff(filename: str) -> None:
        """
        Compares the current version of a file with its last committed version. Prints the differences in a unified diff format.

        Args:
            filename (str): The name of the file to compare.

        Returns:
            None

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If the file is not found in the repository's status or commits.
        """
        working_dir = os.getcwd()
        file_path = os.path.join(working_dir, filename)
        if not os.path.exists(file_path):
            print(f"File: {filename} does not exist")
            return
        status_file_hash = None
        Status.sync()
        status_records = Status.all()
        for record in status_records:
            if record.filename == filename:
                status_file_hash = record.hash
                break
        if status_file_hash == None:
            print(f"File {filename} was not found in the current working directory.")
            return
        all_commits = Commit.all()
        commit_file_hash = None
        for commit in all_commits:
            for record in commit._manifest:
                if record.filename == filename:
                    commit_file_hash = record.hash
                    break
        if commit_file_hash == None:
            print(f"No commit with {filename} was not found to perform a diff.")
            return
        _, file_extension = os.path.splitext(filename)
        path_of_newest_file = os.path.join(working_dir, filename)
        path_of_second_file = os.path.join(working_dir, ".tig\\backup", f"{commit_file_hash}{file_extension}")
        with open(path_of_newest_file, "r") as new_file, open(path_of_second_file, "r") as old_file:
            new_file_lines = new_file.readlines()
            old_file_lines = old_file.readlines()
            diff = unified_diff(
                old_file_lines, new_file_lines, fromfile=f"{filename} (old)", tofile=f"{filename} (new)", lineterm=""
            )
            print("\n".join(diff))

    @staticmethod
    def is_repository() -> bool:
        """
        Checks if the current working directory is a TIG repository.

        Returns:
            bool: True if the current working directory is a TIG repository, False otherwise.
        """
        return os.path.isdir(os.path.join(os.getcwd(), ".tig"))


if __name__ == "__main__":
    """
    Main entry point for the tig version control system. Forwards the commands to the `Parser`.
    """
    from parser import Parser

    Parser.parse()
