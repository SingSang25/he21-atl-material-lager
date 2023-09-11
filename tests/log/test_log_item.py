from tests.config.config import (
    client,
    override_get_db,
)
from he21_atl_material_lager.services.users import get_user_by_username
from he21_atl_material_lager.services.logs import get_logs_by_user_id

pytest_plugins = ["tests.config.fixture"]

def test_log_item_create(valid_token_admin):
    pass

def test_log_item_update(valid_token_admin):
    pass

def test_log_item_delete(valid_token_admin):
    pass