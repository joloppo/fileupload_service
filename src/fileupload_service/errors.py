class StoredFileNotFoundError(Exception):
    """Raised when a file is not found in the storage."""


class StoredFileAlreadyExistsError(Exception):
    """Raised when a file with the same hash already exists in the storage."""
