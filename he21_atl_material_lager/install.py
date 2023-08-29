from fastapi import Depends
from sqlalchemy.orm import Session

from he21_atl_material_lager.schemas.users import UserCreate
from he21_atl_material_lager.services.users import get_user_by_username, create_user
from he21_atl_material_lager.dependencies import get_db


def init_db_user(db: Session = Depends(get_db)):
    default_user = get_user_by_username(db, "admin")
    if not default_user:
        create_user(
            db,
            UserCreate(
                username="admin",
                email="admin@admin.local",
                password="admin",
                admin=True,
                disabled=False,
            ),
        )
