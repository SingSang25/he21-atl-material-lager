from uuid import uuid4

from he21_atl_material_lager.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_uuid():
    return str(uuid4())
