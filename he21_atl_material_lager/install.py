from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.orm import Session

from he21_atl_material_lager.models.user import User
from he21_atl_material_lager.schemas.logs import LogCreate
from he21_atl_material_lager.schemas.users import UserCreate, UserUpdate
from he21_atl_material_lager.dependencies import get_db
from he21_atl_material_lager.services.logs import create_log as create_log_service
from he21_atl_material_lager.services.users import create_user, update_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = next(get_db())
    admin_user = UserCreate(
        username="admin",
        email="admin@bananna.local",
        password="admin",
        admin=True,
        disabled=False,
    )
    user_user = UserCreate(
        username="user",
        email="user@bananna.local",
        password="user",
        admin=False,
        disabled=False,
    )

    create_default_user(db, admin_user)
    create_default_user(db, user_user)
    yield


def create_default_user(db: Session, user: UserCreate):
    if not db.query(User).filter(User.admin == user.admin).first():
        db_user = db.query(User).filter(User.username == user.username).first()
        if db_user is None:
            db_user = create_user(db, user)
            log_text = f"{user.username} User created"
        else:
            db_user = update_user(db, db_user.id, UserUpdate(admin=True), db_user)
            log_text = f"{user.username} User updated"
        create_log_service(
            db,
            LogCreate(
                created_by="system",
                user_id=db_user.id,
                log=log_text,
                type="system",
            ),
        )
