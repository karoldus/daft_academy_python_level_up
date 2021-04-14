from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

# od tego miejsca możemy pisać dowolne testy
def test_read_main(): # nazwa powinna zaczynać się od test_, aby był uruchamiany automatycznie
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}