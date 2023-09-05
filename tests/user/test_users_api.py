from tests.config.config import (
    client,
    create_user_with_return_response,
)

pytest_plugins = ["tests.config.fixture"]


def test_user_create(valid_token):
    response = client.post(
        "/users/",
        json={
            "email": "deadpool@example.com",
            "username": "deadpool",
            "password": "chimichangas4life",
            "admin": False,
            "disabled": False,
        },
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "email" in data
    assert "username" in data
    assert "id" in data


def test_user_get(valid_token, create_user_admin):
    # Get user id
    user_id = create_user_admin

    # Test get user
    response = client.get(
        f"/users/{user_id}", headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "test_admin@bananna.local"
    assert data["username"] == "test_admin"
    assert data["id"] == user_id
    assert data["admin"] == True
    assert data["disabled"] == False


def test_user_get_list(valid_token, create_user_admin, create_user_user):
    # Get user id
    admin_id = create_user_admin
    user_id = create_user_user

    response = client.get(f"/users", headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["username"] == "test_admin" or data[1]["username"] == "test_admin"
    assert (
        data[0]["email"] == "test_admin@bananna.local"
        or data[1]["email"] == "test_admin@bananna.local"
    )
    assert data[0]["id"] == admin_id or data[1]["id"] == admin_id

    assert data[0]["username"] == "test_user" or data[1]["username"] == "test_user"
    assert (
        data[0]["email"] == "test_user@bananna.local"
        or data[1]["email"] == "test_user@bananna.local"
    )
    assert data[0]["id"] == user_id or data[1]["id"] == user_id


def test_user_no_password_returned(valid_token):
    response = create_user_with_return_response(valid_token)

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert "id" in data
    assert "password" not in data
    user_id = data["id"]

    response = client.get(
        f"/users/{user_id}", headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert "password" not in data
    assert data["id"] == user_id

    response = client.get(f"/users", headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert "password" not in data[0]


def test_user_unique_email(valid_token):
    response = create_user_with_return_response(valid_token)
    assert response.status_code == 200

    response = create_user_with_return_response(valid_token, username="secend_deadpool")
    assert response.status_code == 400
    data = response.json()

    assert data["detail"] == "Email already registered"


def test_user_unique_username(valid_token):
    response = create_user_with_return_response(valid_token)
    assert response.status_code == 200

    response = create_user_with_return_response(
        valid_token, email="secend_deadpool@example.com"
    )
    assert response.status_code == 400
    data = response.json()

    assert data["detail"] == "Username already registered"


def test_user_unique_username_and_email(valid_token):
    response = create_user_with_return_response(valid_token)
    assert response.status_code == 200

    response = create_user_with_return_response(valid_token)
    assert response.status_code == 400
    data = response.json()

    assert data["detail"] == "Email and Username already registered"


def test_user_patch_all_propety(valid_token):
    # Create user
    response = create_user_with_return_response(valid_token)
    assert response.status_code == 200, response.text
    data = response.json()
    user_id = data["id"]

    response = client.patch(
        f"/users/{user_id}",
        json={
            "email": "neu_deadpool@example.com",
            "username": "neu_deadpool",
            "password": "neu_chimichangas4life",
            "admin": True,
            "disabled": False,
        },
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 200
    response = client.get(
        f"/users/{user_id}", headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "neu_deadpool@example.com"
    assert data["username"] == "neu_deadpool"
    assert data["id"] == user_id


def test_user_patch_username(valid_token):
    response = create_user_with_return_response(valid_token)
    assert response.status_code == 200, response.text
    data = response.json()
    user_id = data["id"]

    response = client.patch(
        f"/users/{user_id}",
        json={"username": "neu_deadpool"},
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 200
    response = client.get(
        f"/users/{user_id}", headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert data["username"] == "neu_deadpool"
    assert data["id"] == user_id


def test_user_patch_email(valid_token):
    response = create_user_with_return_response(valid_token)
    assert response.status_code == 200, response.text
    data = response.json()
    user_id = data["id"]

    response = client.patch(
        f"/users/{user_id}",
        json={
            "email": "neu_deadpool@example.com",
        },
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 200
    response = client.get(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "neu_deadpool@example.com"
    assert data["username"] == "deadpool"
    assert data["id"] == user_id


def test_user_patch_password(valid_token):
    # Create user
    response = create_user_with_return_response(valid_token)
    assert response.status_code == 200, response.text
    data = response.json()
    user_id = data["id"]

    response = client.patch(
        f"/users/{user_id}",
        json={"password": "neu_chimichangas4life"},
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 200
    response = client.get(
        f"/users/{user_id}", headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert data["username"] == "deadpool"
    assert data["id"] == user_id


def test_user_patch_admin(valid_token):
    response = create_user_with_return_response(valid_token)
    assert response.status_code == 200, response.text
    data = response.json()
    user_id = data["id"]

    response = client.patch(
        f"/users/{user_id}",
        json={
            "admin": False,
        },
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 200
    response = client.get(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert data["username"] == "deadpool"
    assert data["id"] == user_id
    assert data["admin"] == False
    assert data["disabled"] == False


def test_user_patch_disable(valid_token):
    response = create_user_with_return_response(valid_token)
    assert response.status_code == 200, response.text
    data = response.json()
    user_id = data["id"]

    response = client.patch(
        f"/users/{user_id}",
        json={
            "disabled": True,
        },
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 200
    response = client.get(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert data["username"] == "deadpool"
    assert data["id"] == user_id
    assert data["admin"] == True
    assert data["disabled"] == True


def test_user_get_not_found(valid_token):
    response = client.get(
        "/users/uuid_that_does_not_exist",
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "User not found"


def test_user_patch_not_found(valid_token):
    response = client.patch(
        "/users/uuid_that_does_not_exist",
        json={
            "email": "neu_deadpool@example.com",
        },
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "User not found"


def test_user_delete(valid_token):
    response = create_user_with_return_response(valid_token)
    assert response.status_code == 200, response.text
    data = response.json()
    user_id = data["id"]
    response = client.get(
        f"/users/{user_id}", headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200, response.text
    response = client.delete(
        f"/users/{user_id}", headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200, response.text
    response = client.get(
        f"/users/{user_id}", headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "User not found"


def test_user_get_me(valid_token):
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "test_admin@bananna.local"
    assert data["username"] == "test_admin"


def test_user_patch_me(valid_token):
    response = client.patch(
        "/users/me",
        json={"email": "new_test_admin@bananna.local"},
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "new_test_admin@bananna.local"
    assert data["username"] == "test_admin"


def test_user_delete_me(valid_token):
    response = client.delete(
        "/users/me", headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "User deleted"}
