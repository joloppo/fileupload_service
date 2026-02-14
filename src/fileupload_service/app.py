from fastapi import FastAPI

from fileupload_service.routers import file_router

app = FastAPI()

app.include_router(file_router.router, prefix="/files", tags=["files"])
