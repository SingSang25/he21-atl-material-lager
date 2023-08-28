from fastapi import APIRouter, Depends
from typing import Annotated

from he21_atl_material_lager.schemas.users import User
from he21_atl_material_lager.services.users_authenticate import get_current_user

router = APIRouter(prefix="/status")


@router.get("/", tags=["Status"])
async def read_system_status(current_user: Annotated[User, Depends(get_current_user)]):
    return {"status": "ok"}
