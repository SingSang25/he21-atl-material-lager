from tests.config.config import override_get_db

from he21_atl_material_lager.models.user import User
from he21_atl_material_lager.install import lifespan

pytest_plugins = ["tests.config.fixture"]


# Geht nicht, da lifespan nicht in test_db speichert sindern in der echten DB
def test_default_user_create():
    lifespan()
    db = next(override_get_db())
    user = db.query(User).filter(User.username == "admin").first()
    assert user.username == "admin"


def test_no_admin():
    pass


def test_no_user():
    pass


def test_no_admin_false_right():
    pass


def test_no_user_false_right():
    pass
