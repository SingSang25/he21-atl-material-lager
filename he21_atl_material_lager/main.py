from fastapi import FastAPI
from he21_atl_material_lager.database import engine
from he21_atl_material_lager.models import item, log, user
from he21_atl_material_lager.routes import items, logs, users, tockens, status
from he21_atl_material_lager.install import init_db_user
from sqlalchemy.orm import sessionmaker

item.Item.metadata.create_all(bind=engine)
log.Log.metadata.create_all(bind=engine)
user.User.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
db = Session()
init_db_user(db)

app = FastAPI()

app.include_router(items.router)
app.include_router(logs.router)
app.include_router(users.router)
app.include_router(tockens.router)
app.include_router(status.router)

# Fragen:
# Wie kann ich Konfigs speichern? (SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES)
# Wie kann ich die Datenbank mit Daten füllen beim erstellen (User)?
