def test_signup_success(client):
    response = client.post("/auth/signup", json={
        'email': "newuser@test.com",
        'password': "password123"
    })

    assert response.status_code in (200, 201)


def test_login_success(client, test_user):
    response = client.post("/auth/login", json=test_user)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_duplicate_signup_returns_domain_error_payload(client):
    payload = {
        "email": "duplicate-domain-error@test.com",
        "password": "password123",
    }

    first_response = client.post("/auth/signup", json=payload)
    second_response = client.post("/auth/signup", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json() == {
        "code": "CONFLICT",
        "message": "Email already registered",
        "details": {},
    }

