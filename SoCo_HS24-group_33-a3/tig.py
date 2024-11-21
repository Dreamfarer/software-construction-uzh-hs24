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


if __name__ == "__main__":
    from parser import Parser

    Parser.parse()
