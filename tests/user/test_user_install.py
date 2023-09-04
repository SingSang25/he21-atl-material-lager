from fastapi.testclient import TestClient

from tests.config.config import override_get_db, app
from he21_atl_material_lager.dependencies import get_db

from he21_atl_material_lager.models.user import User

pytest_plugins = ["tests.config.fixture"]


# Geht nicht, da startup nicht in test_db speichert
def test_default_user_create(valid_token):
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        db = next(override_get_db())
        user = db.query(User).filter(User.username == "admin").first()
        assert user.username == "admin"
