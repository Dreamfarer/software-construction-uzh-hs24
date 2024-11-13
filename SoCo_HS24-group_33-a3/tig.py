class Backup:
    """Class that handles all the backup-ing; moving, deleting files and so on."""

    @staticmethod
    def create(files: list[str]) -> None:
        """
        Create a backup of provided files.
        """
        pass

    @staticmethod
    def checkout(id: str) -> None:
        """
        Restore the directory's files to the state of a specific commit ID. Use the 'Commit' class to get the files you need to move.
        """
        pass


class Commit:
    """
    Class that can be instanciated to represent one single commit but also serves all other functionalities that have to do with committing.
    """

    def __init__(self, date: str, message: str, manifests: list[tuple[str, str]]) -> None:
        def __unique_id() -> str:
            """
            Generate a unique ID to identify the commit.
            """
            pass

        self.__configuration = {"id": __unique_id(), "date": date, "message": message, "manifests": manifests}

    @staticmethod
    def commit(message: str) -> None:
        """
        Add a new commit_xxx.json file containing the commit ID (unique), commit date and commit message along with all previously staged manifests. Remove the newly commited files from the 'staged.json' file. Add the timestamp in the filename. Copy the files to the backup.
        """
        pass

    @staticmethod
    def all() -> list["Commit"]:
        """
        Return all commits (oldest first, newest last)
        """

        def __read() -> list["Commit"]:
            """Convert the commit_xxx.json file to a 'Commit' object"""
            pass

    @staticmethod
    def latest() -> "Commit":
        """
        Return the most recent commit.
        """
        return Commit.all()[-1]

    def id(self) -> str:
        """
        Return the unique ID of the commit.
        """
        pass

    def manifests(self) -> list[tuple[str, str]]:
        """
        Get all manifests in this commit as a tuple of (filename, hash)
        """
        pass

    def files(self) -> list[str]:
        """
        Get all file names in this commit as a string.
        """

    def __str__(self) -> str:
        """
        String representation of this object. Used when printing via Print(some_commit).
        """
        id = self.__configuration["id"]
        date = self.__configuration["date"]
        message = self.__configuration["message"]
        return f"[{id} | {date} | {message}]"  # TO-DO: Make prettier


class Stage:
    """
    Class that cannot be instanciated. Only serves all functionality related to staging.
    """

    @staticmethod
    def add(filenames: str | list[str]) -> None:
        """
        Add the provided files to the 'staged.json' file containg all currently stated files.
        """
        pass

    @staticmethod
    def remove(filenames: str | list[str]) -> None:
        """
        Remove provided files from the 'staged.json' file.
        """
        pass

    @staticmethod
    def current_manifests() -> list[tuple[str, str]]:
        """
        Return a list of manifests that are currently staged (return the 'staged.json' file content).
        """
        pass


class TIG:
    """
    Class that holds all functionality which is tig general or simply does not belong to committing and staging.
    """

    @staticmethod
    def init(dir: str) -> None:
        """Create a new '.tig/' folder inside the provided path."""
        pass

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
    def manifest() -> list[tuple[str, str]]:
        """
        Get the manifest of each file in the current working directory as a tuple of (filename, hash)
        """

        def hash(path: str) -> str:
            """
            Calculate the hash from the file content.
            """
            pass

    @staticmethod
    def get_untracked_files() -> list[str]:
        """Return the list of files that are not staged (get with Stage.current()) and are also not commited (get with Commit.latest().files())"""
        pass

    @staticmethod
    def get_modified_files() -> list[str]:
        """
        Return a list of files that have a different manifest than in the latest commit. Use 'TIG.manifest()' to get all manifests and 'Commit.latest().manifests()' to get the manifests of the latest commit.
        """
        pass


def main() -> None:
    """
    Main entry point for tig. Parses command-line arguments and calls the corresponding functions.
    """
    import argparse

    parser = argparse.ArgumentParser(description="A simple version control system called tig")
    subparsers = parser.add_subparsers(dest="command")

    # Command for 'init'
    init_parser = subparsers.add_parser("init", help="Initialize a version control repository")
    init_parser.add_argument("directory", type=str, help="Directory to initialize the repository in")

    # Command for 'add'
    add_parser = subparsers.add_parser("add", help="Add a file to the staged state")
    add_parser.add_argument("filename", type=str, help="File to move to the staged state")

    # Command for 'commit'
    commit_parser = subparsers.add_parser("commit", help="Commit all staged files with a message")
    commit_parser.add_argument("commit_message", type=str, help="Message for the commit")

    # Command for 'log'
    log_parser = subparsers.add_parser("log", help="Show the commit history")
    log_parser.add_argument("-N", type=int, default=5, help="Number of recent commits to display")

    # Command for 'status'
    status_parser = subparsers.add_parser("status", help="Show the current status of files")

    # Command for 'diff'
    diff_parser = subparsers.add_parser("diff", help="Show differences for a file")
    diff_parser.add_argument("filename", type=str, help="File to show differences for")

    # Command for 'checkout'
    checkout_parser = subparsers.add_parser("checkout", help="Restore files to a specific commit state")
    checkout_parser.add_argument("commit_id", type=str, help="Commit ID to checkout")

    args = parser.parse_args()

    if args.command == "init":
        TIG.init(args.directory)
    elif args.command == "add":
        Stage.add(args.filename)
    elif args.command == "commit":
        Commit.commit(args.commit_message)
    elif args.command == "log":
        TIG.log(args.N)
    elif args.command == "status":
        TIG.status()
    elif args.command == "diff":
        TIG.diff(args.filename)
    elif args.command == "checkout":
        Backup.checkout(args.commit_id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
