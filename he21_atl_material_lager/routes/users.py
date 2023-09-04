from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
import re

from he21_atl_material_lager.schemas.users import User, UserCreate, UserUpdate
from he21_atl_material_lager.schemas.logs import Log
from he21_atl_material_lager.dependencies import get_db
from he21_atl_material_lager.services.logs import get_logs_by_user_id
from he21_atl_material_lager.services.users_authenticate import get_current_active_user
from he21_atl_material_lager.services.security import get_password_hash
from he21_atl_material_lager.services.users import (
    get_user_by_email,
    get_user_by_username,
    create_user as create_user_service,
    update_user as update_user_service,
    delete_user as delete_user_service,
    get_users,
    get_user_by_id,
)

# Regex for email validation (99% accurate, https://uibakery.io/regex-library/email-regex-python)
regex = re.compile(
    r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
)

router = APIRouter(prefix="/users")


@router.get("/", response_model=list[User], tags=["User"])
def read_users(
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=User, tags=["User"])
def create_user(
    user: UserCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_user_email = get_user_by_email(db, user.email)
    db_user_username = get_user_by_username(db, user.username)
    if not regex.match(user.email):
        raise HTTPException(status_code=400, detail="Email not valid")
    if db_user_email and db_user_username:
        raise HTTPException(
            status_code=400, detail="Email and Username already registered"
        )
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    if db_user_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user_service(db=db, user=user)


@router.get("/me/", response_model=User, tags=["User"])
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@router.patch("/me/", response_model=User, tags=["User"])
def update_user_me(
    user_data: UserUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_user = get_user_by_id(db, current_user.id)

    if user_data.password:
        user_data.password = get_password_hash(user_data.password)
    if user_data.email is not None:
        if not regex.match(user_data.email):
            raise HTTPException(status_code=400, detail="Email not valid")

    return update_user_service(db, current_user.id, user_data, db_user)


@router.delete("/me/", response_model=User, tags=["User"])
def delete_user_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_user = get_user_by_id(db, current_user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    delete_user_service(db, current_user.id)
    return db_user


@router.get("/{user_id}", response_model=User, tags=["User"])
def read_user(
    user_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.patch("/{user_id}", response_model=User, tags=["User"])
def update_user(
    user_data: UserUpdate,
    user_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_data.email is not None:
        if not regex.match(user_data.email):
            raise HTTPException(status_code=400, detail="Email not valid")

    return update_user_service(db, user_id, user_data, db_user)


@router.delete("/{user_id}", response_model=User, tags=["User"])
def delete_user(
    user_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    delete_user_service(db, user_id)
    return db_user


@router.get("/{user_id}/logs", response_model=list[Log], tags=["User"])
def read_user_logs(
    user_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_user = get_logs_by_user_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="No Log by this user")
    return db_user
