from commit import Commit
from status import Status
import os
from difflib import unified_diff


class TIG:
    """
    Class that holds all functionality which is tig general or simply does not belong to committing and staging.
    """

    @staticmethod
    def init(dir: str) -> None:
        """Create a new '.tig/' folder inside the provided path."""
        path = os.path.join(dir, ".tig")
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def log(number: int) -> None:
        """
        Print the commit ID, commit date, and commit message of the last N commits. If -N is not given, the default N=5 is used.
        Essentially pretty print the string representation of each commit of 'Commit.all()'
        """
        commits = sorted(Commit.all(), key=lambda commit: commit._date)
        for commit in commits[:-number]:
            print(f"commit {commit._id}")
            print(f"Date:   {commit._date}")
            print(f"\n    {commit._message}\n")

    @staticmethod
    def diff(filename: str) -> None:
        """
        Compare the current version of the file with its last committed version. Print the differences in a unified diff format. Use a library for this.
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
        Check if the currect working directory is a tig-repository.
        """
        return os.path.isdir(os.path.join(os.getcwd(), ".tig"))


if __name__ == "__main__":
    from parser import Parser

    Parser.parse()
