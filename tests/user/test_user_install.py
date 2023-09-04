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
from he21_atl_material_lager.models.user import User
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
    db = override_get_db()
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


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_default_user_create(valid_token):
    with TestClient(app) as client:
        response = client.get(
            "/users/",
            headers={"Authorization": f"Bearer {valid_token}"},
        )
        db = override_get_db()
        user = db.query(User).filter(User.username == "admin").first()
        assert user.username == "admin"
