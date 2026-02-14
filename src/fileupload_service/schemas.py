from pydantic import BaseModel


class StoredFileInfo(BaseModel):
    id: str
    hash: str

    meta_mime_type: str | None = None
    meta_size_bytes: int | None = None

    def __hash__(self):
        return hash(self.id)


class StoredFile(BaseModel):
    info: StoredFileInfo
    content: bytes
