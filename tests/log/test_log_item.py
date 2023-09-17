from tests.config.config import (
    client,
    override_get_db,
    create_item,
)

from he21_atl_material_lager.services.logs import get_logs_by_id, get_logs_by_item_id

pytest_plugins = ["tests.config.fixture"]


def test_log_item_create(valid_token_admin, create_user_admin):
    response = create_item(valid_token_admin, create_user_admin)
    assert response.status_code == 200, response.text
    data_user = response.json()

    data_user = data_user["logs"][0]

    db_data = get_logs_by_id(next(override_get_db()), data_user["id"])

    assert db_data.log == "Item created"
    assert db_data.type == "item"
    assert db_data.created_by == create_user_admin
    assert db_data.user_id == None


def test_log_item_update(valid_token_admin, create_user_admin, create_user_user):
    response = create_item(valid_token_admin, create_user_admin)
    assert response.status_code == 200, response.text
    data = response.json()
    item_id = data["id"]

    response = client.patch(
        f"/items/{item_id}",
        json={
            "number": 22,
            "item": "foo2",
            "availability": False,
            "position": "Halle 666",
            "user_id": create_user_user,
        },
        headers={"Authorization": f"Bearer {valid_token_admin}"},
    )

    assert response.status_code == 200, response.text

    data_user = response.json()

    data_user = data_user["logs"][1]

    db_data = get_logs_by_id(next(override_get_db()), data_user["id"])

    assert db_data.log == "Item updated"
    assert db_data.type == "item"
    assert db_data.created_by == create_user_admin
    assert db_data.user_id == None


def test_log_item_delete(valid_token_admin, create_user_admin, valid_token_user):
    response = create_item(valid_token_admin, create_user_admin)
    assert response.status_code == 200, response.text
    data = response.json()
    item_id = data["id"]

    response = client.delete(
        f"/items/{item_id}", headers={"Authorization": f"Bearer {valid_token_admin}"}
    )
    assert response.status_code == 200, response.text

    db_data = get_logs_by_item_id(next(override_get_db()), item_id)

    db_data = db_data[1]

    assert db_data.log == "Item deleted"
    assert db_data.type == "item"
    assert db_data.created_by == create_user_admin
    assert db_data.user_id == None
