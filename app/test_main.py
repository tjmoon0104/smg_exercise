from fastapi.testclient import TestClient

from main import app
from service import get_max_id_from_storage

client = TestClient(app)


# GET Request tests
def test_get_sentences_sentence_id():
    """Get a sentence by Id and the rot13 encryption of it"""
    response = client.get("/sentences/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "text": "Texas",
        "cyphered_text": "Grknf"
    }


def test_sentence_path_not_int():
    """Sentence ID is not integer"""
    response = client.get("/sentences/test")
    assert response.status_code == 400
    assert "Invalid ID supplied" in response.json()["detail"]


def test_sentence_not_exist():
    """Sentence does not exist in the storage"""
    response = client.get("/sentences/999999999")
    assert response.status_code == 404
    assert "Sentence not found" in response.json()["detail"]


# POST Request Tests
def test_post_sentences_():
    """Add a new sentence to the store"""
    test_id = get_max_id_from_storage() + 1
    response = client.post(
        "/sentences/",
        json={"id": test_id, "text": "super movie title"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": test_id,
        "text": "super movie title",
        "cyphered_text": "fhcre zbivr gvgyr"
    }


def test_post_existing_sentences():
    """Sentence ID already exist in the storage"""
    response = client.post(
        "/sentences/",
        json={"id": 1, "text": "super movie title"},
    )
    assert response.status_code == 409
    assert "Sentence ID exists" in response.json()["detail"]


def test_id_type_check():
    """id is not integer"""
    response = client.post(
        "/sentences/",
        json={"id": "test", "text": "super movie title"},
    )
    assert response.status_code == 405
    assert "Invalid input" in response.json()["detail"]


def test_text_type_check():
    """text is not string"""
    response = client.post(
        "/sentences/",
        json={"id": 88888888, "text": 1234.5678},
    )
    assert response.status_code == 405
    assert "Invalid input" in response.json()["detail"]


def test_id_null_check():
    """id is null"""
    response = client.post(
        "/sentences/",
        json={"id": None, "text": "super movie title"},
    )
    assert response.status_code == 405
    assert "Invalid input" in response.json()["detail"]


def test_text_null_check():
    """text is null"""
    response = client.post(
        "/sentences/",
        json={"id": 88888888, "text": None},
    )
    assert response.status_code == 405
    assert "Invalid input" in response.json()["detail"]
