from contextlib import asynccontextmanager
from fastapi import FastAPI

from he21_atl_material_lager.models.user import User
from he21_atl_material_lager.schemas.logs import LogCreate
from he21_atl_material_lager.schemas.users import UserCreate, UserUpdate
from he21_atl_material_lager.dependencies import get_db
from he21_atl_material_lager.services.logs import create_log as create_log_service
from he21_atl_material_lager.services.users import (
    create_user,
    update_user,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = next(get_db())
    if not db.query(User).filter(User.admin == True).first():
        if db.query(User).filter(User.username == "admin"):
            create_user(
                db,
                UserCreate(
                    username="admin",
                    email="admin@bananna.local",
                    password="admin",
                    admin=True,
                    disabled=False,
                ),
            )
            create_log_service(
                db,
                LogCreate(
                    user_id="",
                    item_id="",
                    log="User created admin from fist install",
                    type="system",
                ),
            )
        else:
            user = db.query(User).filter(User.username == "admin").first()
            update_user(db, user.id, UserUpdate(admin=True), user)
            create_log_service(
                db,
                LogCreate(
                    user_id="",
                    item_id="",
                    log="User updated admin from no admin in db",
                    type="system",
                ),
            )

    if not db.query(User).filter(User.admin == False).first():
        if db.query(User).filter(User.username == "user"):
            create_user(
                db,
                UserCreate(
                    username="user",
                    email="user@bananna.local",
                    password="user",
                    admin=False,
                    disabled=False,
                ),
            )
            create_log_service(
                db,
                LogCreate(
                    user_id="",
                    item_id="",
                    log="User created user from fist install",
                    type="system",
                ),
            )
        else:
            user = db.query(User).filter(User.username == "user").first()
            update_user(db, user.id, UserUpdate(admin=False), user)
            create_log_service(
                db,
                LogCreate(
                    user_id="",
                    item_id="",
                    log="User updated user from no user in db",
                    type="system",
                ),
            )
    yield
