from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from fileupload_service.routers import file_router


def build_app() -> FastAPI:
    app = FastAPI()
    app.include_router(file_router.router, prefix="/v1/file", tags=["File"])

    @app.get("/")
    async def root():
        return RedirectResponse("/docs", status_code=301)

    return app
