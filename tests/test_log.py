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
    client.post(
        "/users/",
        json={
            "email": "deadpool@example.com",
            "username": "deadpool",
            "password": "chimichangas4life",
        },
    )
    client.post(
        "/items/",
        json={
            "number": 20,
            "item": "foo",
            "availability": True,
            "position": "Halle 1",
            "user_id": 1,
        },
    )


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_log_create():
    response = client.post(
        "/logs/",
        json={
            "user_id": 1,
            "item_id": 1,
            "log": "create",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "user_id" in data
    assert "item_id" in data
    assert "log" in data
    assert "datum" in data


def test_log_get():
    response = client.post(
        "/logs/",
        json={
            "user_id": 1,
            "item_id": 1,
            "log": "create",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    log_id = data["id"]
    log_date = data["datum"]
    response = client.get(f"/logs/{log_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["user_id"] == 1
    assert data["item_id"] == 1
    assert data["log"] == "create"
    assert data["datum"] == log_date


def test_item_get_list():
    response = client.post(
        "/logs/",
        json={
            "user_id": 1,
            "item_id": 1,
            "log": "create",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    log_id_eins = data["id"]
    response = client.post(
        "/logs/",
        json={
            "user_id": 1,
            "item_id": 1,
            "log": "update User from 1 to 2",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    log_id_zwei = data["id"]
    response = client.get(f"/logs")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["user_id"] == 1
    assert data[0]["item_id"] == 1
    assert data[0]["log"] == "create"
    assert data[0]["id"] == log_id_eins
    assert data[1]["user_id"] == 1
    assert data[1]["item_id"] == 1
    assert data[1]["log"] == "update User from 1 to 2"
    assert data[1]["id"] == log_id_zwei


def test_log_get_not_found():
    response = client.post(
        "/logs/",
        json={
            "user_id": 1,
            "item_id": 1,
            "log": "create",
        },
    )
    response = client.get(f"/logs/5")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Log not found"


def test_log_create_user_not_found():
    response = client.post(
        "/logs/",
        json={
            "user_id": 5,
            "item_id": 1,
            "log": "create",
        },
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "User not registered"


def test_log_create_item_not_found():
    response = client.post(
        "/logs/",
        json={
            "user_id": 1,
            "item_id": 5,
            "log": "create",
        },
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Item not registered"


def test_log_create_user_and_item_not_found():
    response = client.post(
        "/logs/",
        json={
            "user_id": 5,
            "item_id": 5,
            "log": "create",
        },
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "User and Item already registered"
