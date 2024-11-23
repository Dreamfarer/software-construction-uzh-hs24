from tig import TIG
from backup import Backup
from commit import Commit
from stage import Stage
from status import Status


class Parser:
    """
    Class that holds all functionality for command-line parsing.
    """

    @staticmethod
    def parse() -> None:
        """
        Parse command-line arguments and call the corresponding functions.
        """

        import argparse

        parser = argparse.ArgumentParser(description="A simple version control system called tig")
        subparsers = parser.add_subparsers(dest="command")

        # Command for 'init'
        init_parser = subparsers.add_parser("init", help="Initialize a version control repository")
        init_parser.add_argument(
            "directory", type=str, nargs="?", default=".", help="Directory to initialize the repository in"
        )

        # Command for 'add'
        add_parser = subparsers.add_parser("add", help="Add a file to the staged state")
        add_parser.add_argument("filename", type=str, help="File to move to the staged state")

        # Command for 'commit'
        commit_parser = subparsers.add_parser("commit", help="Commit all staged files with a message")
        commit_parser.add_argument("commit_message", type=str, help="Message for the commit")

        # Command for 'log'
        log_parser = subparsers.add_parser("log", help="Show the commit history")
        log_parser.add_argument("N", type=int, default=5, help="Number of recent commits to display")

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
            return TIG.init(args.directory)
        if not TIG.is_repository():
            return print("No repository has been found. Create it first with 'python tig.py init <path>'")
        Status.sync()
        if args.command == "add":
            Stage.add(args.filename)
        elif args.command == "commit":
            Commit.commit(args.commit_message)
        elif args.command == "log":
            TIG.log(args.N)
        elif args.command == "status":
            Status.status()
        elif args.command == "diff":
            TIG.diff(args.filename)
        elif args.command == "checkout":
            Backup.checkout(args.commit_id)
        else:
            parser.print_help()
