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
    def manifest() -> list[tuple[str, str]]:
        """
        Return a list of the records that are currently staged (return the 'staged.json' file content).
        """
        pass
