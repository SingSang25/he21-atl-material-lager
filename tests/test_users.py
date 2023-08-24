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


def test_create_user():
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


def test_get_user():
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


def test_get_user_list():
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


def test_unique_email():
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


def test_unique_username():
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
