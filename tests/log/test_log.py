from tests.config.config import (
    client,
    override_get_db,
)
from he21_atl_material_lager.services.users import get_user_by_username
from he21_atl_material_lager.services.logs import get_logs_by_user_id

pytest_plugins = ["tests.config.fixture"]


def test_log_get(valid_token_admin):
    pass

def get_log_by_user_id(valid_token_admin):
    pass

def get_log_by_log_id(valid_token_admin):
    pass

def get_log_by_log_type(valid_token_admin):
    pass

def get_log_by_created_by(valid_token_admin):
    pass