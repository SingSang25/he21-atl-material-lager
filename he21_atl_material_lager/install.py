from sqlalchemy.orm import Session

from he21_atl_material_lager.schemas.users import UserCreate, UserUpdate
from he21_atl_material_lager.models.user import User
from he21_atl_material_lager.services.users import (
    create_user,
    update_user,
)


def init_db_user(db: Session):
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
        else:
            user = db.query(User).filter(User.username == "admin").first()
            update_user(db, user.id, UserUpdate(admin=True), user)

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
        else:
            user = db.query(User).filter(User.username == "user").first()
            update_user(db, user.id, UserUpdate(admin=False), user)
