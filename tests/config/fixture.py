from pytest import fixture

from tests.config.config import (
    engine,
    client,
    override_get_db,
)

from he21_atl_material_lager.database import Base
from he21_atl_material_lager.schemas.users import UserCreate
from he21_atl_material_lager.services.users import (
    get_user_by_username,
    create_user as create_user_servic,
)


@fixture(scope="function", autouse=True)
def clear_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


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
