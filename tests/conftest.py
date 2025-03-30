import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope='module') #module-level(runs once per session)
def client():
    return TestClient(app)
