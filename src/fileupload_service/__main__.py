import uvicorn

uvicorn.run("fileupload_service.app:build_app", reload=False, host="127.0.0.1", port=8000)
