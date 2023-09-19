from pytest import mark

from tests.config.config import (
    override_get_db,
)

from he21_atl_material_lager.models.user import User
from he21_atl_material_lager.schemas.users import UserCreate, UserUpdate
from he21_atl_material_lager.install import create_default_user
from he21_atl_material_lager.services.users import update_user

pytest_plugins = ["tests.config.fixture"]


@mark.disable_autouse
def test_create_admin():
    db = next(override_get_db())
    user = UserCreate(
        username="new_test_admin",
        email="new_test_admin@localhost.ch",
        password="new_test_admin",
        admin=True,
        disabled=False,
    )
    create_default_user(db, user)

    db_user = db.query(User).filter(User.username == user.username).first()

    assert db_user.username == user.username
    assert db_user.email == user.email
    assert db_user.admin == user.admin
    assert db_user.disabled == user.disabled


@mark.disable_autouse
def test_create_user():
    db = next(override_get_db())
    user = UserCreate(
        username="new_test_user",
        email="new_test_user@localhost.ch",
        password="new_test_user",
        admin=False,
        disabled=False,
    )
    create_default_user(db, user)

    db_user = db.query(User).filter(User.username == user.username).first()

    assert db_user.username == user.username
    assert db_user.email == user.email
    assert db_user.admin == user.admin
    assert db_user.disabled == user.disabled


def test_patch_admin(create_user_admin):
    db = next(override_get_db())

    db_user = db.query(User).filter(User.id == create_user_admin).first()

    user = UserCreate(
        username=db_user.username,
        email=db_user.email,
        password=db_user.password,
        admin=False,
        disabled=db_user.disabled,
    )

    update_user(db, create_user_admin, user, db_user)

    assert db_user.admin == False

    user.admin = True

    create_default_user(db, user)

    db_user = db.query(User).filter(User.username == db_user.username).first()

    assert db_user.username == "test_admin"
    assert db_user.email == "test_admin@bananna.local"
    assert db_user.admin == True
    assert db_user.disabled == False
