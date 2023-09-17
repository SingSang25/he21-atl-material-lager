from tests.config.config import (
    client,
)

pytest_plugins = ["tests.config.fixture"]


def test_log_get(valid_token_admin, valid_token_user):
    response = client.get(
        "/logs/", headers={"Authorization": f"Bearer {valid_token_admin}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert "id" in data[0]
    assert "datum" in data[0]
    assert "log" in data[0]
    assert "type" in data[0]
    assert "created_by" in data[0]
    assert "user_id" in data[0]
    assert "item_id" in data[0]


def test_get_log_by_user_id(valid_token_admin, create_user_admin):
    response = client.get(
        f"/logs/{create_user_admin}",
        headers={"Authorization": f"Bearer {valid_token_admin}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data[0]["user_id"] == create_user_admin


def test_get_log_by_log_id(valid_token_admin):
    assert False


def test_get_log_by_log_type(valid_token_admin):
    assert False


def test_get_log_by_created_by(valid_token_admin):
    assert False
