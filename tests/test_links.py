def test_stats(client):
    create = client.post("/links/shorten", json={
        "original_url": "https://google.com",
        "custom_alias": None,
        "expires_at": None
    })

    short_code = create.json()["short_url"].split("/")[-1]

    response = client.get(f"/links/{short_code}/stats")

    assert response.status_code == 200


def test_delete(client):
    create = client.post("/links/shorten", json={
        "original_url": "https://google.com",
        "custom_alias": None,
        "expires_at": None
    })

    short_code = create.json()["short_url"].split("/")[-1]

    response = client.delete(f"/links/{short_code}")

    assert response.status_code == 200


def test_update(client):
    create = client.post("/links/shorten", json={
        "original_url": "https://google.com",
        "custom_alias": None,
        "expires_at": None
    })

    short_code = create.json()["short_url"].split("/")[-1]

    response = client.put(f"/links/{short_code}?new_url=https://yandex.ru")

    assert response.status_code == 200
