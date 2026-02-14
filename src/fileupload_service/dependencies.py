from typing import Annotated
from fastapi import Depends
from fileupload_service.errors import StoredFileAlreadyExistsError, StoredFileNotFoundError
from fileupload_service.schemas import StoredFile, StoredFileInfo


class FileStorage:
    def __init__(self) -> None:
        self.storage: dict[str, StoredFile] = {}
        self.hash_to_id: dict[str, str] = {}

    def save_file(self, StoredFile) -> None:
        if StoredFile.info.id in self.storage:  # Checking by id first as its easier for the user
            raise StoredFileAlreadyExistsError(f"File with id {StoredFile.info.id} already exists")
        if StoredFile.info.hash in self.hash_to_id:
            raise StoredFileAlreadyExistsError(f"File with hash {StoredFile.info.hash} already exists")

        self.storage[StoredFile.info.id] = StoredFile
        self.hash_to_id[StoredFile.info.hash] = StoredFile.info.id

    def get_file_by_id(self, file_id: str) -> StoredFile:
        file = self.storage.get(file_id)
        if file is None:
            raise StoredFileNotFoundError(f"File with id {file_id} not found")
        return file

    def get_file_by_hash(self, file_hash: str) -> StoredFile:
        file_id = self.hash_to_id.get(file_hash)
        if file_id is None:
            raise StoredFileNotFoundError(f"File with hash {file_hash} not found")
        return self.get_file_by_id(file_id)

    def list_files(self) -> list[StoredFileInfo]:
        return [file.info for file in self.storage.values()]

    def delete_file_by_id(self, file_id: str) -> StoredFile:
        file = self.storage.pop(file_id, None)
        if file is None:
            raise StoredFileNotFoundError(f"File with id {file_id} not found")
        self.hash_to_id.pop(file.info.hash)
        return file

    def delete_file_by_hash(self, file_hash: str) -> StoredFile:
        file_id = self.hash_to_id.pop(file_hash, None)
        if file_id is None:
            raise StoredFileNotFoundError(f"File with hash {file_hash} not found")
        file = self.storage.pop(file_id, None)
        assert file is not None, "Inconsistent state: hash_to_id and storage are out of sync"
        return file


_GLOBAL_FILE_STORAGE = FileStorage()  # TODO: Maybe not global?


def get_storage() -> FileStorage:
    return _GLOBAL_FILE_STORAGE


FileStorageDep = Annotated[FileStorage, Depends(get_storage)]
