from fastapi.testclient import TestClient
from router import router
from pathlib import Path
from storage import storage
from models import MemStorage
import requests

client = TestClient(router)


def test_root():
    response = client.get('/')
    assert response.status_code == 200


def test_upload():
    response = client.post('/memes', files={'file': 'test.txt'})
    assert response.status_code == 200


def test_delete():
    response = client.delete('/memes/1')
    assert response.status_code == 200


def test_db_exists():
    db_file = Path.cwd().glob('*.db')
    if db_file:
        assert True


def check_storage():
    response = requests.get('http://127.0.0.1:9000')
    assert response.status_code == 200


def test_storage_bucket():
    assert storage.check_bucket() == "Bucket exists: test"


def test_db_connection():
    assert MemStorage.get_mem_all() is not None



