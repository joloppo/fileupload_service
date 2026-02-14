from typing import Annotated

from fastapi import APIRouter, File, UploadFile, Form

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: Annotated[
        UploadFile, File()
    ],  # Note: UploadFile uses a temp file and spills to disk
    description: Annotated[str, Form()],
):
    print(f"Received file: {file.filename} with description: {description}")
    CHUNK_SIZE = 1024

    MAX_FILESIZE = 10 * 1024 * 1024  # 10 MB
    current_filesize = 0

    buffer = bytearray()
    while current_filesize < MAX_FILESIZE:
        chunk = await file.read(CHUNK_SIZE)
        if not chunk:
            break  # EOF
        buffer.extend(chunk)
        current_filesize += len(chunk)

    if current_filesize >= MAX_FILESIZE:
        return  # TODO: failure

    print(f"Total filesize read: {current_filesize} bytes")
    # TODO: persist to memory


@router.get("")
async def get_uploaded_files():
    pass


@router.delete("/{file_id}")
async def delete_uploaded_file():
    pass
