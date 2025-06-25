from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["username"] == "string"

def test_create_user():
    response = client.post(
        "/register/",
        json={"username": "testuser", "email": "testuser@example.com",
              "full_name": "Test User", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"

def test_auth_flow():
    # Регистрация
    reg_response = client.post(
        "/register/",
        json={"username": "auth_test", "email": "auth@test.com",
              "password": "testpass"}
    )
    assert reg_response.status_code == 200
    
    # Аутентификация
    auth_response = client.post(
        "/token",
        data={"username": "auth_test", "password": "testpass"}
    )
    assert auth_response.status_code == 200
    token = auth_response.json()["access_token"]
    
    # Проверка доступа
    me_response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert me_response.status_code == 200
    assert me_response.json()["username"] == "auth_test"