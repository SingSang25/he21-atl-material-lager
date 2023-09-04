from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from pytest import fixture

from he21_atl_material_lager.database import Base
from he21_atl_material_lager.main import app
from he21_atl_material_lager.dependencies import get_db
from he21_atl_material_lager.services.users import (
    get_user_by_username,
    create_user as create_user_servic,
)
from he21_atl_material_lager.services.items import (
    get_items,
    create_item as create_item_servic,
)
from he21_atl_material_lager.schemas.users import UserCreate
from he21_atl_material_lager.schemas.items import ItemCreate


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


def create_item(create_user_admin):
    db = next(override_get_db())
    create_item_servic(
        db,
        ItemCreate(
            item="test_item",
            number=20,
            position="Halle 1",
            availability=False,
            user_id=create_user_admin,
        ),
    )
    data = get_items(db, 0, 100)
    return data[0].id


def create_log_post(valid_token, user_id, item_id, log="create a new item"):
    response = client.post(
        "/logs/",
        json={"user_id": user_id, "item_id": item_id, "log": log},
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


def test_log_create(valid_token, create_user_admin):
    user_id = create_user_admin
    item_id = create_item(user_id)
    response = create_log_post(valid_token, user_id, item_id)

    assert response.status_code == 200, response.text
    data = response.json()
    assert "user_id" in data
    assert "item_id" in data
    assert "log" in data
    assert "datum" in data


def test_log_get(valid_token, create_user_admin):
    user_id = create_user_admin
    item_id = create_item(user_id)
    response = create_log_post(valid_token, user_id, item_id)

    assert response.status_code == 200, response.text
    data = response.json()

    log_id = data["id"]
    log_date = data["datum"]
    response = client.get(
        f"/logs/{log_id}", headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["user_id"] == user_id
    assert data["item_id"] == item_id
    assert data["log"] == "create a new item"
    assert data["datum"] == log_date


def test_item_get_list(valid_token, create_user_admin):
    user_id = create_user_admin
    item_id = create_item(user_id)
    response = create_log_post(valid_token, user_id, item_id)

    assert response.status_code == 200, response.text
    data = response.json()
    log_id_eins = data["id"]

    response = create_log_post(valid_token, user_id, item_id, log="update User")
    assert response.status_code == 200, response.text
    data = response.json()
    log_id_zwei = data["id"]
    response = client.get(f"/logs", headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["user_id"] == user_id
    assert data[0]["item_id"] == item_id
    assert data[0]["log"] == "create a new item"
    assert data[0]["id"] == log_id_eins
    assert data[1]["user_id"] == user_id
    assert data[1]["item_id"] == item_id
    assert data[1]["log"] == "update User"
    assert data[1]["id"] == log_id_zwei


def test_log_get_not_found(valid_token, create_user_admin):
    response = client.get(
        "/logs/uuid_that_does_not_exist",
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Log not found"


def test_log_create_user_not_found(valid_token, create_user_admin):
    item_id = create_item(create_user_admin)
    response = create_log_post(valid_token, "uuid_that_does_not_exist", item_id)
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "User not registered"


def test_log_create_item_not_found(valid_token, create_user_admin):
    response = create_log_post(
        valid_token, create_user_admin, "uuid_that_does_not_exist"
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Item not registered"


def test_log_create_user_and_item_not_found(valid_token, create_user_admin):
    response = create_log_post(
        valid_token, "uuid_that_does_not_exist", "uuid_that_does_not_exist"
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "User and Item already registered"
