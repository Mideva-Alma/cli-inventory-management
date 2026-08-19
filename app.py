from flask import Flask, request
import requests

app = Flask(__name__)

inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brand": "Silk",
        "price": 5.99,
        "stock": 20,
        "barcode": "0123456789012"
    },
    {
        "id": 2,
        "product_name": "Whole Grain Bread",
        "brand": "Nature's Own",
        "price": 3.49,
        "stock": 15,
        "barcode": "0123456789013"
    },
    {
        "id": 3,
        "product_name": "Peanut Butter",
        "brand": "Jif",
        "price": 4.99,
        "stock": 10,
        "barcode": "0123456789014"
    }
]

def fetch_product_from_api(barcode):
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"

    headers = {
        "User-Agent": "InventoryManagementSystem/1.0"
    }

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        return None

    data = response.json()

    if data.get("status") != 1:
        return None

    product = data.get("product", {})

    return {
        "product_name": product.get("product_name"),
        "brand": product.get("brands"),
        "ingredients_text": product.get("ingredients_text"),
        "barcode": barcode
    }

@app.route("/")
def home():
    return {"message": "Inventory Management API is running"}


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return inventory


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return item

    return {"error": "Inventory item not found"}, 404

@app.route("/inventory", methods=["POST"])
def add_inventory_item():
    data = request.get_json()

    new_item = {
        "id": len(inventory) + 1,
        "product_name": data["product_name"],
        "brand": data["brand"],
        "price": data["price"],
        "stock": data["stock"],
        "barcode": data["barcode"]
    }

    inventory.append(new_item)

    return new_item, 201

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    data = request.get_json()

    for item in inventory:
        if item["id"] == item_id:
            if "product_name" in data:
                item["product_name"] = data["product_name"]

            if "brand" in data:
                item["brand"] = data["brand"]

            if "price" in data:
                item["price"] = data["price"]

            if "stock" in data:
                item["stock"] = data["stock"]

            if "barcode" in data:
                item["barcode"] = data["barcode"]

            return item

    return {"error": "Inventory item not found"}, 404

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)
            return {"message": "Inventory item deleted successfully"}

    return {"error": "Inventory item not found"}, 404

@app.route("/products/<barcode>", methods=["GET"])
def find_product(barcode):
    product = fetch_product_from_api(barcode)

    if product is None:
        return {"error": "Product not found"}, 404

    return product

@app.route("/inventory/from-api/<barcode>", methods=["POST"])
def add_product_from_api(barcode):
    product = fetch_product_from_api(barcode)

    if product is None:
        return {"error": "Product not found in OpenFoodFacts"}, 404

    new_item = {
        "id": len(inventory) + 1,
        "product_name": product["product_name"],
        "brand": product["brand"],
        "price": 0.0,
        "stock": 0,
        "barcode": product["barcode"],
        "ingredients_text": product["ingredients_text"]
    }

    inventory.append(new_item)

    return new_item, 201

if __name__ == "__main__":
    app.run(debug=True)