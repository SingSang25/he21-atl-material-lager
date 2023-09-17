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
from he21_atl_material_lager.services.logs import create_log as create_log_service
from he21_atl_material_lager.schemas.logs import LogCreate, Log


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
def valid_token_admin():
    response = client.post(
        "/login/access-token",
        data={
            "username": "test_admin",
            "password": "test_admin",
        },
    )
    data = response.json()
    return data["access_token"]


@fixture(scope="function")
def valid_token_user():
    response = client.post(
        "/login/access-token",
        data={
            "username": "test_user",
            "password": "test_user",
        },
    )
    data = response.json()
    return data["access_token"]


@fixture(scope="function")
def create_logs():
    db = next(override_get_db())
    db_log = create_log_service(
        db,
        LogCreate(
            log="test_log_1",
            type="test_type_1",
            user_id="user_id_1",
            item_id="item_id_1",
            created_by="created_by_1",
        ),
    )
    create_log_service(
        db,
        LogCreate(
            log="test_log_2",
            type="test_type_2",
            user_id="user_id_2",
            item_id="item_id_2",
            created_by="created_by_2",
        ),
    )
    create_log_service(
        db,
        LogCreate(
            log="test_log_3",
            type="test_type_3",
            user_id="user_id_3",
            item_id="item_id_3",
            created_by="created_by_3",
        ),
    )
    create_log_service(
        db,
        LogCreate(
            log="test_log_1",
            type="test_type_1",
            user_id="user_id_1",
            item_id="item_id_1",
            created_by="created_by_2",
        ),
    )
    create_log_service(
        db,
        LogCreate(
            log="test_log_1",
            type="test_type_1",
            user_id="user_id_3",
            item_id="item_id_1",
            created_by="created_by_1",
        ),
    )

    return (
        db_log.id,
        db_log.datum,
        db_log.log,
        db_log.type,
        db_log.created_by,
        db_log.user_id,
        db_log.item_id,
    )
