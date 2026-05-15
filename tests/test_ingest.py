from datetime import datetime
from pydantic_schemas.ingest import OperationIngestInput


VALID_PAYLOAD = {
    "op_operation_type": "MAS",
    "op_cause": "avarie",
    "op_means": "oui",
    "op_author": "michel",
    "op_author_category": "Autorité militaire française à terre",
    "op_cross": "Polynésie",
    "pa_depts": "999",
    "op_is_metro": True,
    "op_event": "jen sais rien",
    "op_event_category": "Accidents individuels à personnes",
    "op_authority": "Affaires maritimes",
    "op_second_authority": None,
    "op_responsability_zone": "Responsabilité française",
    "pa_lat": "4.98",
    "pa_lng": "1.52",
    "pa_wind_direction": "42",
    "pa_wind_strength": 5,
    "pa_sea_strength": 8,
    "pa_start_date": "2026-05-01 00:00:00",
    "pa_end_date": "2026-05-06 05:15:00",
    "pa_time_zone": "Pacific/Tahiti",
    "pa_system": "secmarweb",
    "human_res": [
        {"personn_category": "Commerce français", "number": "3", "result": "Personne assistée"},
        {"personn_category": "Clandestin", "number": "1", "result": "Personne décédée"},
    ],
    "floats": [
        {
            "order_number": "1",
            "flag": "Français",
            "type": "bateau",
            "float_state": "Retrouvé après recherche",
            "category": "Plaisance",
            "immatriculation": "jambonneau",
        }
    ],
}


def test_ingest_creates_operation(client):
    response = client.post("/ingest/", json=VALID_PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    assert "operation_id" in data
    assert data["type_operation"] == "MAS"


def test_ingest_date_validation_fails(client):
    payload = {**VALID_PAYLOAD, "pa_start_date": "2026-05-10 00:00:00", "pa_end_date": "2026-05-01 00:00:00"}
    response = client.post("/ingest/", json=payload)
    assert response.status_code == 422


def test_ingest_extra_fields_ignored(client):
    payload = {**VALID_PAYLOAD, "params": {}, "part": 4, "FormSubmitter:float_part_form-Create floats": False}
    response = client.post("/ingest/", json=payload)
    assert response.status_code == 201


def test_parse_date_valid():
    model = OperationIngestInput(**VALID_PAYLOAD)
    dt = model.parse_date("2026-05-01 00:00:00")
    assert dt == datetime(2026, 5, 1, 0, 0, 0)


def test_parse_date_invalid_returns_none():
    model = OperationIngestInput(**VALID_PAYLOAD)
    assert model.parse_date("not-a-date") is None


def test_parse_date_none_returns_none():
    model = OperationIngestInput(**VALID_PAYLOAD)
    assert model.parse_date(None) is None
