from flask import Flask, request

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


if __name__ == "__main__":
    app.run(debug=True)