from fastapi.testclient import TestClient
from tests.config.config import override_get_db, app

from he21_atl_material_lager.models.user import User

pytest_plugins = ["tests.config.fixture"]


# Geht nicht, da lifespan nicht in test_db speichert sindern in der echten DB
def test_default_user_create():
    with TestClient(app) as client:
        db = next(override_get_db())
        user = db.query(User).filter(User.username == "admin").first()
        assert user.username == "admin"
