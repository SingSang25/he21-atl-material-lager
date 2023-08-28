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


def test_item_create():
    response = client.post(
        "/items/",
        json={
            "number": 20,
            "item": "foo",
            "availability": True,
            "position": "Halle 1",
            "user_id": 1,
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "item" in data
    assert "number" in data
    assert "availability" in data
    assert "position" in data
    assert "user_id" in data


def test_item_get():
    response = client.post(
        "/items/",
        json={
            "number": 20,
            "item": "foo",
            "availability": True,
            "position": "Halle 1",
            "user_id": 1,
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    item_id = data["id"]
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["number"] == 20
    assert data["item"] == "foo"
    assert data["availability"] == True
    assert data["position"] == "Halle 1"
    assert data["user_id"] == 1


def test_item_get_list():
    response = client.post(
        "/items/",
        json={
            "number": 20,
            "item": "foo",
            "availability": True,
            "position": "Halle 1",
            "user_id": 1,
        },
    )
    assert response.status_code == 200, response.text
    response = client.post(
        "/items/",
        json={
            "number": 202,
            "item": "foo2",
            "availability": True,
            "position": "Halle 2",
            "user_id": 2,
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    item_id = data["id"]
    response = client.get(f"/items")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["number"] == 20
    assert data[0]["item"] == "foo"
    assert data[0]["availability"] == True
    assert data[0]["position"] == "Halle 1"
    assert data[0]["user_id"] == 1
    assert data[1]["number"] == 202
    assert data[1]["item"] == "foo2"
    assert data[1]["availability"] == True
    assert data[1]["position"] == "Halle 2"
    assert data[1]["user_id"] == 2


def test_item_patch_all_propety():
    response = client.post(
        "/items/",
        json={
            "number": 20,
            "item": "foo",
            "availability": True,
            "position": "Halle 1",
            "user_id": 1,
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    item_id = data["id"]
    response = client.patch(
        f"/items/{item_id}",
        json={
            "number": 22,
            "item": "foo2",
            "availability": False,
            "position": "Halle 666",
            "user_id": 99,
        },
    )
    assert response.status_code == 200
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["number"] == 22
    assert data["item"] == "foo2"
    assert data["availability"] == False
    assert data["position"] == "Halle 666"
    assert data["user_id"] == 99


def test_item_patch_number():
    response = client.post(
        "/items/",
        json={
            "number": 20,
            "item": "foo",
            "availability": True,
            "position": "Halle 1",
            "user_id": 1,
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    item_id = data["id"]
    response = client.patch(
        f"/items/{item_id}",
        json={
            "number": 22,
        },
    )
    assert response.status_code == 200
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["number"] == 22
    assert data["item"] == "foo"
    assert data["availability"] == True
    assert data["position"] == "Halle 1"
    assert data["user_id"] == 1


def test_item_patch_item():
    response = client.post(
        "/items/",
        json={
            "number": 20,
            "item": "foo",
            "availability": True,
            "position": "Halle 1",
            "user_id": 1,
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    item_id = data["id"]
    response = client.patch(
        f"/items/{item_id}",
        json={
            "item": "foo2",
        },
    )
    assert response.status_code == 200
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["number"] == 20
    assert data["item"] == "foo2"
    assert data["availability"] == True
    assert data["position"] == "Halle 1"
    assert data["user_id"] == 1


def test_item_patch_availability():
    response = client.post(
        "/items/",
        json={
            "number": 20,
            "item": "foo",
            "availability": True,
            "position": "Halle 1",
            "user_id": 1,
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    item_id = data["id"]
    response = client.patch(
        f"/items/{item_id}",
        json={
            "availability": False,
        },
    )
    assert response.status_code == 200
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["number"] == 20
    assert data["item"] == "foo"
    assert data["availability"] == False
    assert data["position"] == "Halle 1"
    assert data["user_id"] == 1


def test_item_patch_position():
    response = client.post(
        "/items/",
        json={
            "number": 20,
            "item": "foo",
            "availability": True,
            "position": "Halle 1",
            "user_id": 1,
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    item_id = data["id"]
    response = client.patch(
        f"/items/{item_id}",
        json={
            "position": "Halle 666",
        },
    )
    assert response.status_code == 200
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["number"] == 20
    assert data["item"] == "foo"
    assert data["availability"] == True
    assert data["position"] == "Halle 666"
    assert data["user_id"] == 1


def test_item_patch_user_id():
    response = client.post(
        "/items/",
        json={
            "number": 20,
            "item": "foo",
            "availability": True,
            "position": "Halle 1",
            "user_id": 1,
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    item_id = data["id"]
    response = client.patch(
        f"/items/{item_id}",
        json={
            "user_id": 99,
        },
    )
    assert response.status_code == 200
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["number"] == 20
    assert data["item"] == "foo"
    assert data["availability"] == True
    assert data["position"] == "Halle 1"
    assert data["user_id"] == 99


def test_item_get_not_found():
    response = client.post(
        "/items/",
        json={
            "number": 20,
            "item": "foo",
            "availability": True,
            "position": "Halle 1",
            "user_id": 1,
        },
    )
    response = client.get(f"/items/5")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Item not found"


def test_item_patch_not_found():
    response = client.patch(
        f"/items/5",
        json={
            "number": 22,
            "item": "foo2",
            "availability": False,
            "position": "Halle 666",
            "user_id": 99,
        },
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Item not found"


def test_item_delete():
    response = client.post(
        "/items/",
        json={
            "number": 20,
            "item": "foo",
            "availability": False,
            "position": "Halle 1",
            "user_id": 1,
        },
    )
    assert response.status_code == 200
    data = response.json()
    item_id = data["id"]
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Item not found"
