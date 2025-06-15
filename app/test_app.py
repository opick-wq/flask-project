import pytest
from app.app import app # <-- PERUBAHAN DI SINI

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Simple Flask API!" in response.data

def test_get_data_endpoint(client):
    response = client.get('/data')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_add_data_endpoint(client):
    new_item = {"id": 3, "name": "keyboard"}
    response = client.post('/data', json=new_item)
    assert response.status_code == 201
    assert response.get_json() == new_item