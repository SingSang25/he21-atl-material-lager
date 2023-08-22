from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from he21_atl_material_lager.models.user import User
from he21_atl_material_lager.schemas.users import UserCreate, UserUpdate


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    fake_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, username=user.username, password=fake_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_data: UserUpdate, db_user: User):
    stored_item_object_schema = UserUpdate(
        username=db_user.username,
        email=db_user.email,
        password=db_user.password,
        id=db_user.id,
    )

    updated_item_model_dump = user_data.model_dump(exclude_unset=True)

    updated_item_object_schema = stored_item_object_schema.model_copy(
        update=updated_item_model_dump
    )

    db.query(User).filter(User.id == user_id).update(
        jsonable_encoder(updated_item_object_schema)
    )
    db.commit()
    return get_user(db, user_id)