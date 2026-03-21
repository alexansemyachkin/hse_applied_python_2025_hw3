def test_register(client):
    response = client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "123"
    })

    assert response.status_code == 200
    assert "user_id" in response.json()


def test_register_duplicate(client):
    client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "123"
    })

    response = client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "123"
    })

    assert response.status_code == 400


def test_login_success(client):
    client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "123"
    })

    response = client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "123"
    })

    assert response.status_code == 200


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "123"
    })

    response = client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "wrong"
    })

    assert response.status_code == 401
