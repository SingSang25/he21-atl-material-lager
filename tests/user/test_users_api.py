from fastapi import Depends
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from he21_atl_material_lager.database import Base
from he21_atl_material_lager.main import app
from he21_atl_material_lager.dependencies import get_db
from he21_atl_material_lager.services.users import (
    get_user_by_username,
    create_user as create_user_servic,
)
from he21_atl_material_lager.schemas.users import UserCreate
from pytest import fixture

SQLALCHEMY_DATABASE_URL = (
    "sqlite:///./he21_atl_material_lager/database/sql_test_item.db"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@fixture(scope="function", autouse=True)
def clear_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@fixture(scope="function")
def valid_token():
    response = client.post(
        "/login/access-token",
        data={
            "username": "test_admin",
            "password": "test_admin",
        },
    )
    data = response.json()
    return data["access_token"]


@fixture(scope="function", autouse=True)
def create_user_admin():
    db = next(override_get_db())
    create_user_servic(
        db,
        UserCreate(
            username="test_admin",
            email="test_admin@bananna.local",
            password="test_admin",
            admin=True,
            disabled=False,
        ),
    )
    data = get_user_by_username(db, "test_admin")
    return data.id


@fixture(scope="function", autouse=True)
def create_user_user():
    db = next(override_get_db())
    create_user_servic(
        db,
        UserCreate(
            username="test_user",
            email="test_user@bananna.local",
            password="test_user",
            admin=False,
            disabled=False,
        ),
    )
    data = get_user_by_username(db, "test_user")
    return data.id


def create_user_with_return_response(
    valid_token,
    email="deadpool@example.com",
    username="deadpool",
    password="chimichangas4life",
    admin=True,
    disabled=False,
):
    response = client.post(
        "/users/",
        json={
            "email": email,
            "username": username,
            "password": password,
            "admin": admin,
            "disabled": disabled,
        },
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    return response


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


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
