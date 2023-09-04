from tests.config.config import client

pytest_plugins = ["tests.config.fixture"]


def test_user_login():
    response = client.post(
        "/login/access-token",
        data={
            "username": "test_admin",
            "password": "test_admin",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data


def test_user_login_wrong_password():
    response = client.post(
        "/login/access-token",
        data={
            "username": "test_admin",
            "password": "test_admin_wrong",
        },
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Incorrect username or password"


def test_user_login_wrong_username():
    response = client.post(
        "/login/access-token",
        data={
            "username": "test_admin_wrong",
            "password": "test_admin",
        },
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Incorrect username or password"
