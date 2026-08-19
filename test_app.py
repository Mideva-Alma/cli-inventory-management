import pytest
from app import app, inventory


@pytest.fixture
def client():
    app.config["TESTING"] = True

    original_inventory = [item.copy() for item in inventory]

    with app.test_client() as client:
        yield client

    inventory.clear()
    inventory.extend(original_inventory)

def test_get_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 3
    assert data[0]["product_name"] == "Organic Almond Milk"

def test_get_inventory_item_valid(client):
    response = client.get("/inventory/1")

    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert data["product_name"] == "Organic Almond Milk"


def test_get_inventory_item_not_found(client):
    response = client.get("/inventory/999")

    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data

def test_add_inventory_item_valid(client):
    new_item = {
        "product_name": "Test Product",
        "brand": "Test Brand",
        "price": 9.99,
        "stock": 5,
        "barcode": "1111111111111"
    }

    response = client.post("/inventory", json=new_item)

    assert response.status_code == 201
    data = response.get_json()
    assert data["product_name"] == "Test Product"
    assert data["id"] == 4


def test_add_inventory_item_missing_fields(client):
    incomplete_item = {
        "product_name": "",
        "brand": "Test Brand",
        "price": 9.99,
        "stock": 5,
        "barcode": "1111111111111"
    }

    response = client.post("/inventory", json=incomplete_item)

    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_update_inventory_item_valid(client):
    response = client.patch("/inventory/1", json={"price": 6.99})

    assert response.status_code == 200
    data = response.get_json()
    assert data["price"] == 6.99
    assert data["id"] == 1


def test_update_inventory_item_not_found(client):
    response = client.patch("/inventory/999", json={"price": 6.99})

    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data

def test_delete_inventory_item_valid(client):
    response = client.delete("/inventory/1")

    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data

    # confirm it's actually gone
    check = client.get("/inventory/1")
    assert check.status_code == 404


def test_delete_inventory_item_not_found(client):
    response = client.delete("/inventory/999")

    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data