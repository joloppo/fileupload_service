from fastapi import HTTPException, status


class StoredFileNotFoundError(HTTPException):
    def __init__(self, detail: str = "File not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class StoredFileAlreadyExistsError(HTTPException):
    def __init__(self, detail: str = "File already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
