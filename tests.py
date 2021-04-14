from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)

# od tego miejsca możemy pisać dowolne testy
def test_read_main(): # nazwa powinna zaczynać się od test_, aby był uruchamiany automatycznie
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_hello_name():
    name = 'Kamila'
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert response.text == f'"Hello {name}"'

# @pytest.mark.parametrize("name", ["Zenek", "Marek", "Alojzy Niezdąży"])
# def test_hello_name(name):
#     response = client.get(f"/hello/{name}")
#     assert response.status_code == 200
#     assert response.text == f'"Hello {name}"

def test_counter():
    response = client.get(f"/counter")
    assert response.status_code == 200
    assert response.text == "1"
    # 2nd Try
    response = client.get(f"/counter")
    assert response.status_code == 200
    assert response.text == "2"