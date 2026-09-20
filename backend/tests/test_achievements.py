def test_get_achievements_unauthorized(client):
    response = client.get("/api/v1/achievements")
    assert response.status_code == 401


def test_get_achievements_empty(auth_client):
    response = auth_client.get("/api/v1/achievements")
    assert response.status_code == 200
    assert response.json() == []


def test_create_achievement(auth_client):
    response = auth_client.post("/api/v1/achievements", json={
        "name": "Первое достижение",
        "description": "Тест"
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Первое достижение"


def test_create_duplicate_achievement(auth_client):
    auth_client.post("/api/v1/achievements", json={
        "name": "Дубликат",
        "description": "Тест"
    })
    response = auth_client.post("/api/v1/achievements", json={
        "name": "Дубликат",
        "description": "Ещё раз"
    })
    assert response.status_code == 400


def test_get_achievements_after_create(auth_client):
    auth_client.post("/api/v1/achievements", json={
        "name": "Тестовая",
        "description": "Проверка"
    })
    response = auth_client.get("/api/v1/achievements")
    assert response.status_code == 200
    assert len(response.json()) >= 1