from tests.config.config import (
    client,
    override_get_db,
)
from he21_atl_material_lager.services.users import get_user_by_username
from he21_atl_material_lager.services.logs import get_logs_by_user_id

pytest_plugins = ["tests.config.fixture"]


def test_log_user_create(valid_token_admin):
    # Test create user
    response = client.post(
        "/users/",
        json={
            "email": "deadpool@example.com",
            "username": "deadpool",
            "password": "chimichangas4life",
            "admin": False,
            "disabled": False,
        },
        headers={"Authorization": f"Bearer {valid_token_admin}"},
    )

    assert response.status_code == 200, response.text
    data = response.json()

    # Get user ids
    user_id = data["id"]
    admin_user_id = get_user_by_username(next(override_get_db()), "test_admin").id

    # Test get user
    response = client.get(
        f"/users/{user_id}", headers={"Authorization": f"Bearer {valid_token_admin}"}
    )

    data = response.json()

    data_log = data["logs"]

    assert data_log[0]["log"] == "User created"
    assert data_log[0]["type"] == "user"
    assert data_log[0]["created_by"] == admin_user_id
    assert data_log[0]["user_id"] == user_id


def test_log_user_update(valid_token_admin):
    # Test create user
    response = client.post(
        "/users/",
        json={
            "email": "deadpool@example.com",
            "username": "deadpool",
            "password": "chimichangas4life",
            "admin": False,
            "disabled": False,
        },
        headers={"Authorization": f"Bearer {valid_token_admin}"},
    )

    assert response.status_code == 200, response.text
    data = response.json()

    # Get user ids
    user_id = data["id"]
    admin_user_id = get_user_by_username(next(override_get_db()), "test_admin").id

    # Test update user
    response = client.patch(
        f"/users/{user_id}",
        json={
            "email": "neu_deadpool@example.com",
            "username": "neu_deadpool",
        },
        headers={"Authorization": f"Bearer {valid_token_admin}"},
    )

    assert response.status_code == 200, response.text
    data = response.json()
    data_log = data["logs"]

    assert data_log[1]["log"] == "User updated"
    assert data_log[1]["type"] == "user"
    assert data_log[1]["created_by"] == admin_user_id
    assert data_log[1]["user_id"] == user_id


def test_log_user_delete(valid_token_admin):
    # Test create user
    response = client.post(
        "/users/",
        json={
            "email": "deadpool@example.com",
            "username": "deadpool",
            "password": "chimichangas4life",
            "admin": False,
            "disabled": False,
        },
        headers={"Authorization": f"Bearer {valid_token_admin}"},
    )

    assert response.status_code == 200, response.text
    data = response.json()

    # Get user ids
    user_id = data["id"]
    admin_user_id = get_user_by_username(next(override_get_db()), "test_admin").id

    # Test delete user
    response = client.delete(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {valid_token_admin}"},
    )

    assert response.status_code == 200, response.text
    data = response.json()
    data_log = get_logs_by_user_id(next(override_get_db()), user_id)

    assert data_log[1].log == "User deleted"
    assert data_log[1].type == "user"
    assert data_log[1].created_by == admin_user_id
    assert data_log[1].user_id == user_id


def test_log_user_me_update(valid_token_admin):
    user_id = get_user_by_username(next(override_get_db()), "test_admin").id
    # Test update user
    response = client.patch(
        "/users/me/",
        json={"email": "neu@neu.neu"},
        headers={"Authorization": f"Bearer {valid_token_admin}"},
    )

    assert response.status_code == 200, response.text
    data = response.json()
    data_log = data["logs"]

    assert data_log[1]["log"] == "User updated"
    assert data_log[1]["type"] == "user"
    assert data_log[1]["created_by"] == user_id
    assert data_log[1]["user_id"] == user_id


def test_log_user_me_delete(valid_token_admin):
    user_id = get_user_by_username(next(override_get_db()), "test_admin").id
    # Test update user
    response = client.delete(
        "/users/me/",
        headers={"Authorization": f"Bearer {valid_token_admin}"},
    )

    assert response.status_code == 200, response.text

    data_log = get_logs_by_user_id(next(override_get_db()), user_id)

    assert data_log[1].log == "User deleted"
    assert data_log[1].type == "user"
    assert data_log[1].created_by == user_id
    assert data_log[1].user_id == user_id