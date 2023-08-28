from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from he21_atl_material_lager.schemas.users import User, UserCreate, UserUpdate
from he21_atl_material_lager.schemas.logs import Log
from he21_atl_material_lager.dependencies import get_db
from he21_atl_material_lager.services.users import (
    get_user_by_email,
    get_user_by_username,
    create_user as create_user_service,
    update_user as update_user_service,
    delete_user as delete_user_service,
    get_users,
    get_user,
)
from he21_atl_material_lager.services.logs import get_logs_by_user_id

router = APIRouter(prefix="/users")


@router.patch("/{user_id}", response_model=User, tags=["User"])
def update_user(user_data: UserUpdate, user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return update_user_service(db, user_id, user_data, db_user)


@router.post("/", response_model=User, tags=["User"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user_email = get_user_by_email(db, user.email)
    db_user_username = get_user_by_username(db, user.username)

    if db_user_email and db_user_username:
        raise HTTPException(
            status_code=400, detail="Email and Username already registered"
        )
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    if db_user_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user_service(db=db, user=user)


@router.get("/", response_model=list[User], tags=["User"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=User, tags=["User"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/{user_id}/logs", response_model=list[Log], tags=["User"])
def read_user_logs(user_id: int, db: Session = Depends(get_db)):
    db_user = get_logs_by_user_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="No Log by this user")
    return db_user


@router.delete("/{user_id}", response_model=User, tags=["User"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    delete_user_service(db, user_id)
    return db_user
