from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from he21_atl_material_lager.database import Base
from he21_atl_material_lager.main import app
from he21_atl_material_lager.dependencies import get_db
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


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_user_create():
    response = client.post(
        "/users/",
        json={
            "email": "deadpool@example.com",
            "username": "deadpool",
            "password": "chimichangas4life",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "email" in data
    assert "username" in data
    assert "id" in data


def test_user_get():
    response = client.post(
        "/users/",
        json={
            "email": "deadpool@example.com",
            "username": "deadpool",
            "password": "chimichangas4life",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    user_id = data["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert data["username"] == "deadpool"
    assert data["id"] == user_id


def test_user_get_list():
    response = client.post(
        "/users/",
        json={
            "email": "deadpool@example.com",
            "username": "deadpool",
            "password": "chimichangas4life",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    user_id = data["id"]
    response = client.get(f"/users")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["email"] == "deadpool@example.com"
    assert "password" not in data[0]
    assert data[0]["id"] == user_id


def test_user_no_password_returned():
    response = client.post(
        "/users/",
        json={
            "email": "deadpool@example.com",
            "username": "deadpool",
            "password": "chimichangas4life",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert "id" in data
    assert "password" not in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert "password" not in data
    assert data["id"] == user_id

    response = client.get(f"/users")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["email"] == "deadpool@example.com"
    assert "password" not in data[0]
    assert data[0]["id"] == user_id


def test_user_unique_email():
    response = client.post(
        "/users/",
        json={
            "email": "deadpool@example.com",
            "username": "deadpool",
            "password": "chimichangas4life",
        },
    )
    assert response.status_code == 200

    response = client.post(
        "/users/",
        json={
            "email": "deadpool@example.com",
            "username": "anderesdeadpool",
            "password": "chimichangas4life",
        },
    )
    assert response.status_code == 400
    data = response.json()

    assert data["detail"] == "Email already registered"


def test_user_unique_username():
    response = client.post(
        "/users/",
        json={
            "email": "deadpool@example.com",
            "username": "deadpool",
            "password": "chimichangas4life",
        },
    )
    assert response.status_code == 200

    response = client.post(
        "/users/",
        json={
            "email": "anderesdeadpool@example.com",
            "username": "deadpool",
            "password": "chimichangas4life",
        },
    )
    assert response.status_code == 400
    data = response.json()

    assert data["detail"] == "Username already registered"


def test_user_unique_username_and_email():
    response = client.post(
        "/users/",
        json={
            "email": "deadpool@example.com",
            "username": "deadpool",
            "password": "chimichangas4life",
        },
    )
    assert response.status_code == 200

    response = client.post(
        "/users/",
        json={
            "email": "deadpool@example.com",
            "username": "deadpool",
            "password": "chimichangas4life",
        },
    )
    assert response.status_code == 400
    data = response.json()

    assert data["detail"] == "Email and Username already registered"


def test_user_patch_all_propety():
    response = client.post(
        "/users/",
        json={
            "email": "deadpool@example.com",
            "username": "deadpool",
            "password": "chimichangas4life",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    user_id = data["id"]
    response = client.patch(
        f"/users/{user_id}",
        json={
            "email": "neu_deadpool@example.com",
            "username": "neu_deadpool",
            "password": "neu_chimichangas4life",
        },
    )
    assert response.status_code == 200
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "neu_deadpool@example.com"
    assert data["username"] == "neu_deadpool"
    assert data["id"] == user_id


def test_user_patch_username():
    response = client.post(
        "/users/",
        json={
            "email": "deadpool@example.com",
            "username": "deadpool",
            "password": "chimichangas4life",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    user_id = data["id"]
    response = client.patch(
        f"/users/{user_id}",
        json={
            "username": "neu_deadpool",
        },
    )
    assert response.status_code == 200
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert data["username"] == "neu_deadpool"
    assert data["id"] == user_id


def test_user_patch_email():
    response = client.post(
        "/users/",
        json={
            "email": "deadpool@example.com",
            "username": "deadpool",
            "password": "chimichangas4life",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    user_id = data["id"]
    response = client.patch(
        f"/users/{user_id}",
        json={
            "email": "neu_deadpool@example.com",
        },
    )
    assert response.status_code == 200
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "neu_deadpool@example.com"
    assert data["username"] == "deadpool"
    assert data["id"] == user_id


def test_user_get_not_found():
    response = client.post(
        "/users/",
        json={
            "email": "deadpool@example.com",
            "username": "deadpool",
            "password": "chimichangas4life",
        },
    )
    assert response.status_code == 200, response.text
    user_id = "5"
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "User not found"


def test_user_patch_not_found():
    response = client.post(
        "/users/",
        json={
            "email": "deadpool@example.com",
            "username": "deadpool",
            "password": "chimichangas4life",
        },
    )
    assert response.status_code == 200, response.text
    user_id = "5"
    response = client.patch(
        f"/users/{user_id}",
        json={
            "email": "neu_deadpool@example.com",
        },
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "User not found"


def test_user_delete():
    response = client.post(
        "/users/",
        json={
            "email": "deadpool@example.com",
            "username": "deadpool",
            "password": "chimichangas4life",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    user_id = data["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "User not found"
