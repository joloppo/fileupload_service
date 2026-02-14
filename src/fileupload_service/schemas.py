from pydantic import BaseModel


class StoredFileInfo(BaseModel):
    id: str
    hash: str


class StoredFile(BaseModel):
    info: StoredFileInfo
    content: bytes
