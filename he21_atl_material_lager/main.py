from fastapi import FastAPI

from he21_atl_material_lager.database import engine
from he21_atl_material_lager.models import item, log, user
from he21_atl_material_lager.routes import items, logs, users, tockens, status
from he21_atl_material_lager.install import lifespan

item.Item.metadata.create_all(bind=engine)
log.Log.metadata.create_all(bind=engine)
user.User.metadata.create_all(bind=engine)

app = FastAPI(lifespan=lifespan)

app.include_router(items.router)
app.include_router(logs.router)
app.include_router(users.router)
app.include_router(tockens.router)
app.include_router(status.router)
