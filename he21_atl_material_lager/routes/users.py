from fastapi import APIRouter
from he21_atl_material_lager.schemas.users import User, UserCreate
from he21_atl_material_lager.schemas.logs import Log, LogCreate    
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from he21_atl_material_lager.dependencies import get_db
from he21_atl_material_lager.services.users import (
    get_user_by_email,
    get_user_by_username,
    create_user as create_user_service,
    get_users,
    get_user,
)

router = APIRouter(prefix="/users")


@router.post("/", response_model=User, tags=["User"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = get_user_by_username(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user_service(db=db, user=user)

@router.get("/", response_model=list[User], tags=["User"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=User, tags=["User"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/{user_id}/logs", response_model=User, tags=["User"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user