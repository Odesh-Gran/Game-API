def test_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"


def test_register_success(client):
    response = client.post("/api/v1/register", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "qwerty123"
    })
    assert response.status_code == 201
    assert response.json()["message"] == "Аккаунт создан!"


def test_register_duplicate(client):
    client.post("/api/v1/register", json={
        "username": "dupuser",
        "email": "dup@example.com",
        "password": "qwerty123"
    })
    response = client.post("/api/v1/register", json={
        "username": "dupuser",
        "email": "dup2@example.com",
        "password": "qwerty123"
    })
    assert response.status_code == 400
    assert "занят" in response.json()["detail"]


def test_login_success(client):
    client.post("/api/v1/register", json={
        "username": "logintest",
        "email": "login@example.com",
        "password": "qwerty123"
    })
    response = client.post("/api/v1/login", json={
        "username": "logintest",
        "password": "qwerty123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    response = client.post("/api/v1/login", json={
        "username": "nonexistent",
        "password": "wrong"
    })
    assert response.status_code == 401