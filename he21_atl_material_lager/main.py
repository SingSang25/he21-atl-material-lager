from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from he21_atl_material_lager.database import engine
from he21_atl_material_lager.models import item, log, user
from he21_atl_material_lager.routes import items, logs, users, tockens, status
from he21_atl_material_lager.dependencies import get_db
from he21_atl_material_lager.install import init_db_user

item.Item.metadata.create_all(bind=engine)
log.Log.metadata.create_all(bind=engine)
user.User.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(items.router)
app.include_router(logs.router)
app.include_router(users.router)
app.include_router(tockens.router)
app.include_router(status.router)


@app.on_event("startup")
def startup_event():
    init_db_user()


# Fragen:
# Wie kann ich Konfigs speichern? (SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES)
# C:\Users\jaze\GitHub\HE21-ATL-Material-Lager\.venv\Lib\site-packages\pydantic\_internal\_config.py:269: UserWarning: Valid config keys have changed in V2:
# * 'orm_mode' has been renamed to 'from_attributes'
#  warnings.warn(message, UserWarning)
