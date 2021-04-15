from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)


def test_counter():
    response = client.get(f"/auth", params={'password':'haslo', 'password_hash':'013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105e5786ceaabd62bbc27336153d0d316b2d13b36804080c44aa6198c533215'})
    assert response.status_code == 204
    # 2nd Try
    response = client.get(f"/auth",params={'password':'haslo', 'password_hash':'013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105e5786ceaabd62bbc27336153d0d316b2d13b36804080c44aa6198c533219'})  
    assert response.status_code == 401

    response = client.get(f"/auth")  
    assert response.status_code == 401

    response = client.get(f"/auth",params={'password':' ', 'password_hash':' '})  
    assert response.status_code == 401