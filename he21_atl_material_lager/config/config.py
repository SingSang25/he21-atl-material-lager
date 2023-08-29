import os
from dotenv import load_dotenv

load_dotenv("he21_atl_material_lager/config/.env")

SECRET_KEY = os.getenv("SECRET_KEY", )
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: float = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
