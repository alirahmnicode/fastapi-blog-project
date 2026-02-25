def test_register_response_201(anon_client):
    payload = {"username": "newuser",
               "email": "new@gmail.com", "password": "12345678", "password_confirm": "12345678"}
    response = anon_client.post("/users/register", json=payload)
    response_data = response.json()
    print(response_data)
    assert response.status_code == 201
    assert "access_token" in response_data
    assert "refresh_token" in response_data


def test_login_response_200(anon_client):
    payload = {
        "username": "testuser",
        "password": "12345678"
    }
    response = anon_client.post("/users/login", json=payload)
    print(response)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def test_login_invalid_data_response_401(anon_client):
    payload = {"username": "testuser", "password": "wrongpassword"}
    response = anon_client.post(
        "/users/login", json=payload)
    assert response.status_code == 401

    payload = {"username": "nonexistentuser", "password": "12345678"}
    response = anon_client.post("/users/login", json=payload)
    assert response.status_code == 401
