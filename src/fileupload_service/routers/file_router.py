import hashlib
from loguru import logger
from typing import Annotated

from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from starlette.responses import Response

from fileupload_service.file_storage import FileStorageDep
from fileupload_service.schemas import StoredFile, StoredFileInfo

router = APIRouter()


@router.post("/upload")
async def upload_file(
    # Note: UploadFile uses a temp file and spills to disk
    file: Annotated[UploadFile, File()],
    file_id: Annotated[str, Form()],  # file_id was mentioned but not elaborated on, so I'm assuming it's a form field
    file_storage: FileStorageDep,
) -> StoredFileInfo:
    logger.info(f"Received file: {file.filename} with file_id: {file_id}")

    # Chunked reading
    CHUNK_SIZE = 1024
    MAX_FILESIZE = 10 * 1024 * 1024  # 10 MB
    current_filesize = 0
    buffer = bytearray()
    hasher = hashlib.sha256()
    while current_filesize <= MAX_FILESIZE:
        chunk = await file.read(CHUNK_SIZE)
        if not chunk:
            break  # EOF
        buffer.extend(chunk)
        hasher.update(chunk)
        current_filesize += len(chunk)

    if current_filesize >= MAX_FILESIZE:
        raise HTTPException(
            status_code=413, detail="File size exceeds the maximum allowed limit"
        )  # TODO: human readable size limit

    # Result
    sha256 = hasher.hexdigest()
    info = StoredFileInfo(
        id=file_id,
        hash=sha256,
        meta_mime_type=file.content_type,
        meta_size_bytes=current_filesize,
    )
    to_store = StoredFile(
        info=info,
        content=bytes(buffer),  # WARNING: consider using memoryview
    )

    # Store
    file_storage.save_file(to_store)  # TODO: error handling into http exceptions

    return info


@router.get("/list_info")
async def list_files(file_storage: FileStorageDep) -> list[StoredFileInfo]:
    return file_storage.list_files()


@router.get("")
async def get_file(file_storage: FileStorageDep, file_id: str | None = None, file_hash: str | None = None) -> Response:
    if (file_id is None and file_hash is None) or (file_id is not None and file_hash is not None):
        raise HTTPException(status_code=400, detail="Must provide one of file_id or file_hash")

    if file_id is not None:
        stored_file = file_storage.get_file_by_id(file_id)
    else:
        stored_file = file_storage.get_file_by_hash(file_hash)

    return Response(
        content=stored_file.content,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{stored_file.info.id}"'},
    )


@router.delete("")
async def delete_uploaded_file(
    file_storage: FileStorageDep, file_id: str | None = None, file_hash: str | None = None
) -> None:
    if (file_id is None and file_hash is None) or (file_id is not None and file_hash is not None):
        raise HTTPException(status_code=400, detail="Must provide one of file_id or file_hash")

    if file_id is not None:
        file_storage.delete_file_by_id(file_id)

    if file_hash is not None:
        file_storage.delete_file_by_hash(file_hash)
