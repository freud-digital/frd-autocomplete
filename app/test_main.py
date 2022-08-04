from fastapi.testclient import TestClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from .main import app
from .config import BASEROW_TABLE_MAPPING, BASEROW_TOKEN, MINIMAL_CHARS_ERROR

NO_MATCH_STRING = "laösdfjsadlökfjasdlköfjsdklöfjsdalföjlkfj"

client = TestClient(app)


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())


def test_read_main():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200


def test_correct_endpoint_number():
    with TestClient(app) as client:
        response = client.get("/")
        endpoints = response.json()['endpoints']
        assert len(endpoints) == len(BASEROW_TABLE_MAPPING.keys()) + 1


def test_for_token():
    assert BASEROW_TOKEN


def test_entity_endpoints():
    with TestClient(app) as client:
        response = client.get("/")
        endpoints = response.json()['endpoints']
        for x in endpoints:
            response = client.get(f"{x['endpoint']}")
            assert response.status_code == 422
            response = client.get(f"{x['endpoint']}?q=ha")
            assert response.status_code == 200
            assert response.json()['data'] == MINIMAL_CHARS_ERROR


def test_minimal_chars():
    with TestClient(app) as client:
        response = client.get("/")
        endpoints = response.json()['endpoints']
        for x in endpoints:
            response = client.get(f"{x['endpoint']}?q=ha")
            assert response.status_code == 200
            assert response.json()['data'] == MINIMAL_CHARS_ERROR


def test_no_match():
    with TestClient(app) as client:
        response = client.get("/")
        endpoints = response.json()['endpoints']
        for x in endpoints:
            response = client.get(f"{x['endpoint']}?q={NO_MATCH_STRING}")
            assert response.status_code == 200
            assert 'tc:suggestion' in response.json().keys()
