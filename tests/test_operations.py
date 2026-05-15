from tests.test_ingest import VALID_PAYLOAD


def test_get_operations_empty(client):
    response = client.get("/operations/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_and_get_operation(client):
    ingest = client.post("/ingest/", json=VALID_PAYLOAD)
    assert ingest.status_code == 201
    op_id = ingest.json()["operation_id"]

    response = client.get(f"/operations/{op_id}")
    assert response.status_code == 200
    assert response.json()["operation_id"] == op_id


def test_get_operation_not_found(client):
    response = client.get("/operations/999999")
    assert response.status_code == 404


def test_update_operation(client):
    ingest = client.post("/ingest/", json=VALID_PAYLOAD)
    op_id = ingest.json()["operation_id"]

    response = client.put(f"/operations/{op_id}", json={"type_operation": "SAR"})
    assert response.status_code == 200
    assert response.json()["type_operation"] == "SAR"


def test_delete_operation(client):
    ingest = client.post("/ingest/", json=VALID_PAYLOAD)
    op_id = ingest.json()["operation_id"]

    response = client.delete(f"/operations/{op_id}")
    assert response.status_code == 204

    response = client.get(f"/operations/{op_id}")
    assert response.status_code == 404
