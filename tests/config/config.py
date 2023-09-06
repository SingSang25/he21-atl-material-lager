from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from he21_atl_material_lager.main import app
from he21_atl_material_lager.dependencies import get_db
from he21_atl_material_lager.install import init_db_user

SQLALCHEMY_DATABASE_URL = (
    "sqlite:///./he21_atl_material_lager/database/sql_test_item.db"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def create_user(
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


def create_item(
    valid_token,
    user_id,
    number=20,
    item="foo",
    availability=True,
    position="Halle 1",
):
    response = client.post(
        "/items/",
        json={
            "number": number,
            "item": item,
            "availability": availability,
            "position": position,
            "user_id": user_id,
        },
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    return response


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
