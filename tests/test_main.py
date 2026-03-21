def test_redirect_with_cache(client):
    create = client.post("/links/shorten", json={
        "original_url": "https://google.com",
        "custom_alias": None,
        "expires_at": None
    })

    short_code = create.json()["short_url"].split("/")[-1]

    client.get(f"/{short_code}", follow_redirects=False)

    response = client.get(f"/{short_code}", follow_redirects=False)

    assert response.status_code in (302, 307)


def test_redirect_not_found(client):
    response = client.get("/nope", follow_redirects=False)
    assert response.status_code == 404
