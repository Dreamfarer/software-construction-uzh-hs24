class Backup:
    """
    Class that handles all the backup-ing; moving, deleting files and so on.
    """

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
