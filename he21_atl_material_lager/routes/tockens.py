from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from he21_atl_material_lager.schemas.tokens import Token
from he21_atl_material_lager.services.tokens import create_access_token
from he21_atl_material_lager.dependencies import get_db
from he21_atl_material_lager.services.users_authenticate import authenticate_user
from he21_atl_material_lager.config.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

router = APIRouter(prefix="/login")


@router.post("/access-token/", response_model=Token, tags=["Token"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username},
        secret_key=SECRET_KEY,
        algorithm=ALGORITHM,
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
