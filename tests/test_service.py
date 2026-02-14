import hashlib

from fileupload_service.schemas import StoredFileInfo


def test_simple(client):
    # when
    files_list_initial = client.get("/v1/file/list_info")
    # then
    assert files_list_initial.status_code == 200
    assert files_list_initial.json() == []

    # given
    content = b"Hello, world!"
    content2 = b"Hello, world!2"
    to_insert = StoredFileInfo(
        id="test.txt",
        hash=hashlib.sha256(content).hexdigest(),
    )
    # when
    inserted = client.post(
        "/v1/file/upload", files={"file": (to_insert.id, content, "text/plain")}, data={"file_id": to_insert.id}
    )
    # then
    assert inserted.status_code == 200, inserted.json()
    inserted = StoredFileInfo(**inserted.json())
    assert inserted == to_insert

    # then
    files_list_after = client.get("/v1/file/list_info")
    assert files_list_after.status_code == 200
    assert files_list_after.json() == [to_insert.dict()]

    # get by id
    get_by_id = client.get(f"/v1/file?file_id={to_insert.id}")
    assert get_by_id.status_code == 200
    assert get_by_id.content == content

    # get by hash
    get_by_hash = client.get(f"/v1/file?file_hash={to_insert.hash}")
    assert get_by_hash.status_code == 200
    assert get_by_hash.content == content

    to_insert2 = StoredFileInfo(
        id="test2.txt",
        hash=hashlib.sha256(content2).hexdigest(),
    )
    # when
    inserted2 = client.post(
        "/v1/file/upload", files={"file": (to_insert2.id, content2, "text/plain")}, data={"file_id": to_insert2.id}
    )
    # then
    assert inserted2.status_code == 200, inserted2.json()
    inserted2 = StoredFileInfo(**inserted2.json())
    assert inserted2 == to_insert2

    # then
    files_list_after2 = client.get("/v1/file/list_info")
    assert files_list_after2.status_code == 200
    assert files_list_after2.json() == [to_insert.dict(), to_insert2.dict()]

    # delete by id
    delete_by_id = client.delete(f"/v1/file?file_id={to_insert.id}")
    assert delete_by_id.status_code == 200

    # check 1 left
    files_list_after_delete = client.get("/v1/file/list_info")
    assert files_list_after_delete.status_code == 200
    assert files_list_after_delete.json() == [to_insert2.dict()]

    # delete by hash
    delete_by_hash = client.delete(f"/v1/file?file_hash={to_insert2.hash}")
    assert delete_by_hash.status_code == 200

    # check empty
    files_list_after_delete2 = client.get("/v1/file/list_info")
    assert files_list_after_delete2.status_code == 200
    assert files_list_after_delete2.json() == []
