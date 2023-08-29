from sqlalchemy.orm import Session

from he21_atl_material_lager.schemas.users import UserCreate
from he21_atl_material_lager.services.users import (
    get_user_by_username,
    create_user as create_user_service,
)
from he21_atl_material_lager.dependencies import get_db


def init_db_user():
    db = next(get_db())
    create_user(
        UserCreate(
            username="admin",
            email="admin@test.local",
            password="admin",
            admin=True,
            disabled=False,
        ),
        db=db,
    )
    create_user(
        UserCreate(
            username="user",
            email="user@test.local",
            password="user",
            admin=False,
            disabled=False,
        ),
        db=db,
    )


def create_user(
    user: UserCreate,
    db: Session,
):
    default_user = get_user_by_username(db, user.username)
    if not default_user:
        create_user_service(
            db,
            UserCreate(
                username=user.username,
                email=user.email,
                password=user.password,
                admin=user.admin,
                disabled=user.disabled,
            ),
        )
