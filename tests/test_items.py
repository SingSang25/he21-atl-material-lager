from tests.config.config import client, create_item

pytest_plugins = ["tests.config.fixture"]


def test_item_create(valid_token_admin, create_user_admin):
    response = create_item(valid_token_admin, create_user_admin)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "item" in data
    assert "number" in data
    assert "availability" in data
    assert "position" in data
    assert "user_id" in data


def test_item_create_no_admin(valid_token_user, create_user_user):
    response = create_item(valid_token_user, create_user_user)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Activ User is not an Admin"


def test_item_get(valid_token_user, valid_token_admin, create_user_admin):
    response = create_item(valid_token_admin, create_user_admin)
    assert response.status_code == 200, response.text
    data = response.json()
    item_id = data["id"]

    response = client.get(
        f"/items/{item_id}", headers={"Authorization": f"Bearer {valid_token_user}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["number"] == 20
    assert data["item"] == "foo"
    assert data["availability"] == True
    assert data["position"] == "Halle 1"
    assert data["user_id"] == create_user_admin


def test_item_get_list(valid_token_admin, valid_token_user, create_user_admin):
    response = create_item(valid_token_admin, create_user_admin)
    assert response.status_code == 200, response.text
    data = response.json()
    user_id1 = data["user_id"]

    response = create_item(
        valid_token_admin,
        create_user_admin,
        number=202,
        item="foo2",
        availability=False,
        position="Halle 2",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    user_id2 = data["user_id"]

    response = client.get(
        f"/items", headers={"Authorization": f"Bearer {valid_token_user}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()

    assert data[0]["number"] == 20 or data[1]["number"] == 20
    assert data[0]["item"] == "foo" or data[1]["item"] == "foo"
    assert data[0]["availability"] == True or data[1]["availability"] == True
    assert data[0]["position"] == "Halle 1" or data[1]["position"] == "Halle 1"
    assert data[0]["user_id"] == user_id1 or data[1]["user_id"] == user_id1

    assert data[1]["number"] == 202 or data[0]["number"] == 202
    assert data[1]["item"] == "foo2" or data[0]["item"] == "foo2"
    assert data[1]["availability"] == False or data[0]["availability"] == False
    assert data[1]["position"] == "Halle 2" or data[0]["position"] == "Halle 2"
    assert data[1]["user_id"] == user_id2 or data[0]["user_id"] == user_id2


def test_item_patch_all_propety(
    valid_token_admin, valid_token_user, create_user_admin, create_user_user
):
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
    assert response.status_code == 200
    response = client.get(
        f"/items/{item_id}", headers={"Authorization": f"Bearer {valid_token_user}"}
    )
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["number"] == 22
    assert data["item"] == "foo2"
    assert data["availability"] == False
    assert data["position"] == "Halle 666"
    assert data["user_id"] == create_user_user


def test_item_patch_number(valid_token_admin, valid_token_user, create_user_admin):
    response = create_item(valid_token_admin, create_user_admin)
    assert response.status_code == 200, response.text
    data = response.json()
    item_id = data["id"]
    response = client.patch(
        f"/items/{item_id}",
        json={
            "number": 22,
        },
        headers={"Authorization": f"Bearer {valid_token_user}"},
    )
    assert response.status_code == 200
    response = client.get(
        f"/items/{item_id}", headers={"Authorization": f"Bearer {valid_token_admin}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["number"] == 22
    assert data["item"] == "foo"
    assert data["availability"] == True
    assert data["position"] == "Halle 1"
    assert data["user_id"] == create_user_admin


def test_item_patch_item(valid_token_admin, valid_token_user, create_user_admin):
    response = create_item(valid_token_admin, create_user_admin)
    assert response.status_code == 200, response.text
    data = response.json()
    item_id = data["id"]
    response = client.patch(
        f"/items/{item_id}",
        json={
            "item": "foo2",
        },
        headers={"Authorization": f"Bearer {valid_token_user}"},
    )
    assert response.status_code == 200
    response = client.get(
        f"/items/{item_id}", headers={"Authorization": f"Bearer {valid_token_user}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["number"] == 20
    assert data["item"] == "foo2"
    assert data["availability"] == True
    assert data["position"] == "Halle 1"
    assert data["user_id"] == create_user_admin


def test_item_patch_availability(
    valid_token_admin, valid_token_user, create_user_admin
):
    response = create_item(valid_token_admin, create_user_admin)
    response.status_code == 200, response.text
    data = response.json()
    item_id = data["id"]
    response = client.patch(
        f"/items/{item_id}",
        json={
            "availability": False,
        },
        headers={"Authorization": f"Bearer {valid_token_user}"},
    )
    assert response.status_code == 200
    response = client.get(
        f"/items/{item_id}", headers={"Authorization": f"Bearer {valid_token_user}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["number"] == 20
    assert data["item"] == "foo"
    assert data["availability"] == False
    assert data["position"] == "Halle 1"
    assert data["user_id"] == create_user_admin


def test_item_patch_position(valid_token_admin, valid_token_user, create_user_admin):
    response = create_item(valid_token_admin, create_user_admin)
    assert response.status_code == 200, response.text
    data = response.json()
    item_id = data["id"]
    response = client.patch(
        f"/items/{item_id}",
        json={
            "position": "Halle 666",
        },
        headers={"Authorization": f"Bearer {valid_token_user}"},
    )
    assert response.status_code == 200
    response = client.get(
        f"/items/{item_id}", headers={"Authorization": f"Bearer {valid_token_user}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["number"] == 20
    assert data["item"] == "foo"
    assert data["availability"] == True
    assert data["position"] == "Halle 666"
    assert data["user_id"] == create_user_admin


def test_item_patch_user_id(valid_token_admin, valid_token_user, create_user_admin):
    response = create_item(valid_token_admin, create_user_admin)
    assert response.status_code == 200, response.text
    data = response.json()
    item_id = data["id"]
    response = client.patch(
        f"/items/{item_id}",
        json={
            "user_id": create_user_admin,
        },
        headers={"Authorization": f"Bearer {valid_token_user}"},
    )
    assert response.status_code == 200
    response = client.get(
        f"/items/{item_id}", headers={"Authorization": f"Bearer {valid_token_user}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["number"] == 20
    assert data["item"] == "foo"
    assert data["availability"] == True
    assert data["position"] == "Halle 1"
    assert data["user_id"] == create_user_admin


def test_item_get_not_found(valid_token_admin, create_user_admin):
    response = client.get(
        f"/items/uuid_that_does_not_exist",
        headers={"Authorization": f"Bearer {valid_token_admin}"},
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Item not found"


def test_item_patch_not_found(valid_token_user, create_user_admin):
    response = client.patch(
        "/items/uuid_that_does_not_exist",
        json={
            "number": 22,
            "item": "foo2",
            "availability": False,
            "position": "Halle 666",
            "user_id": create_user_admin,
        },
        headers={"Authorization": f"Bearer {valid_token_user}"},
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Item not found"


def test_item_delete(valid_token_admin, valid_token_user, create_user_admin):
    response = create_item(valid_token_admin, create_user_admin)
    assert response.status_code == 200
    data = response.json()
    item_id = data["id"]
    response = client.get(
        f"/items/{item_id}", headers={"Authorization": f"Bearer {valid_token_user}"}
    )
    assert response.status_code == 200, response.text
    response = client.delete(
        f"/items/{item_id}", headers={"Authorization": f"Bearer {valid_token_admin}"}
    )
    assert response.status_code == 200, response.text
    response = client.get(
        f"/items/{item_id}", headers={"Authorization": f"Bearer {valid_token_user}"}
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Item not found"


def test_item_get_log(valid_token_admin, valid_token_user, create_user_admin):
    response = create_item(valid_token_admin, create_user_admin)
    assert response.status_code == 200
    data = response.json()
    item_id = data["id"]
    response = client.get(
        f"/items/{item_id}/logs",
        headers={"Authorization": f"Bearer {valid_token_user}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data[0]["item_id"] == item_id
    assert data[0]["created_by"] == create_user_admin
    assert data[0]["log"] == "Item created"


def test_item_delete_no_admin(valid_token_user, valid_token_admin, create_user_user):
    response = create_item(valid_token_admin, create_user_user)
    assert response.status_code == 200
    data = response.json()
    item_id = data["id"]
    response = client.delete(
        f"/items/{item_id}", headers={"Authorization": f"Bearer {valid_token_user}"}
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Activ User is not an Admin"
