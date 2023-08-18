from fastapi import FastAPI
from he21_atl_material_lager.models import item
from he21_atl_material_lager.database import engine
from he21_atl_material_lager.routes import items

app = FastAPI()

item.Item.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(items.router)