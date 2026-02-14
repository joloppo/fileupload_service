import pytest
from fastapi.testclient import TestClient
from fileupload_service.app import build_app

from fileupload_service.file_storage import get_storage, FileStorage


@pytest.fixture()
def client():
    app = build_app()
    test_storage = FileStorage()
    app.dependency_overrides[get_storage] = lambda: test_storage

    with TestClient(app) as client:
        yield client
