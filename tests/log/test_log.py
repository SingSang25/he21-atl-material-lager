from tests.config.config import (
    client,
)

pytest_plugins = ["tests.config.fixture"]


def test_log_get(valid_token_admin, create_logs):
    response = client.get(
        "/logs/", headers={"Authorization": f"Bearer {valid_token_admin}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert "id" in data[0]
    assert "log" in data[0]
    assert "type" in data[0]
    assert "user_id" in data[0]
    assert "item_id" in data[0]
    assert "created_by" in data[0]
    assert len(data) == 6  # 5 from fixture + 1 from login for header


def test_get_log_by_user_id(valid_token_admin, create_logs):
    response = client.get(
        f"/users/{create_logs[5]}/logs",
        headers={"Authorization": f"Bearer {valid_token_admin}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert len(data) == 2


def test_get_log_by_log_id(valid_token_admin, create_logs):
    response = client.get(
        f"/logs/{create_logs[0]}",
        headers={"Authorization": f"Bearer {valid_token_admin}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data["id"] == create_logs[0]
    assert data["log"] == "test_log_1"
    assert data["type"] == "test_type_1"
    assert data["user_id"] == "user_id_1"
    assert data["item_id"] == "item_id_1"
    assert data["created_by"] == "created_by_1"


def test_get_log_by_log_type(valid_token_admin, create_logs):
    response = client.get(
        f"/logs/type/{create_logs[3]}",
        headers={"Authorization": f"Bearer {valid_token_admin}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert len(data) == 3
    assert data[0]["id"] == create_logs[0]
    assert data[0]["log"] == "test_log_1"
    assert data[0]["type"] == "test_type_1"
    assert data[0]["user_id"] == "user_id_1"
    assert data[0]["item_id"] == "item_id_1"
    assert data[0]["created_by"] == "created_by_1"


def test_get_log_by_created_by(valid_token_admin, create_logs):
    response = client.get(
        f"/logs/created/{create_logs[4]}",
        headers={"Authorization": f"Bearer {valid_token_admin}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert len(data) == 2
    assert data[0]["id"] == create_logs[0]
    assert data[0]["log"] == "test_log_1"
    assert data[0]["type"] == "test_type_1"
    assert data[0]["user_id"] == "user_id_1"
    assert data[0]["item_id"] == "item_id_1"
    assert data[0]["created_by"] == "created_by_1"
