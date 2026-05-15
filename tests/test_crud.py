from tests.test_ingest import VALID_PAYLOAD


def test_get_flotteurs_empty(client):
    response = client.get("/flotteurs/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_flotteur_created_with_ingest(client):
    ingest = client.post("/ingest/", json=VALID_PAYLOAD)
    op_id = ingest.json()["operation_id"]

    response = client.get(f"/flotteurs/by-operation/{op_id}")
    assert response.status_code == 200
    flotteurs = response.json()
    assert len(flotteurs) == 1
    assert flotteurs[0]["pavillon"] == "Français"


def test_get_flotteur_not_found(client):
    response = client.get("/flotteurs/999999")
    assert response.status_code == 404


def test_human_results_created_with_ingest(client):
    ingest = client.post("/ingest/", json=VALID_PAYLOAD)
    op_id = ingest.json()["operation_id"]

    response = client.get(f"/human-results/by-operation/{op_id}")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2


def test_operation_stats_created_with_ingest(client):
    ingest = client.post("/ingest/", json=VALID_PAYLOAD)
    op_id = ingest.json()["operation_id"]

    response = client.get(f"/operation-stats/by-operation/{op_id}")
    assert response.status_code == 200
    stats = response.json()
    assert len(stats) == 1
    assert stats[0]["annee"] == 2026
    assert stats[0]["mois"] == 5
    assert stats[0]["avec_clandestins"] is True
