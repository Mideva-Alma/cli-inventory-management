import requests

BASE_URL = "http://127.0.0.1:5000"


def view_inventory():
    response = requests.get(f"{BASE_URL}/inventory")

    if response.status_code == 200:
        items = response.json()

        if not items:
            print("Inventory is empty.")
            return

        for item in items:
            print(f"\nID: {item['id']}")
            print(f"Product: {item['product_name']}")
            print(f"Brand: {item['brand']}")
            print(f"Price: ${item['price']}")
            print(f"Stock: {item['stock']}")
            print(f"Barcode: {item['barcode']}")
    else:
        print("Failed to retrieve inventory.")


def view_item():
    item_id = input("Enter inventory ID: ")

    response = requests.get(f"{BASE_URL}/inventory/{item_id}")

    if response.status_code == 200:
        item = response.json()

        print(f"\nID: {item['id']}")
        print(f"Product: {item['product_name']}")
        print(f"Brand: {item['brand']}")
        print(f"Price: ${item['price']}")
        print(f"Stock: {item['stock']}")
        print(f"Barcode: {item['barcode']}")
    else:
        print("Inventory item not found.")


def add_item():
    product_name = input("Product name: ")
    brand = input("Brand: ")
    price = float(input("Price: "))
    stock = int(input("Stock: "))
    barcode = input("Barcode: ")

    item = {
        "product_name": product_name,
        "brand": brand,
        "price": price,
        "stock": stock,
        "barcode": barcode
    }

    response = requests.post(
        f"{BASE_URL}/inventory",
        json=item
    )

    if response.status_code == 201:
        print("\nItem added successfully!")
        print(response.json())
    else:
        print("Failed to add item.")


def update_item():
    item_id = input("Enter inventory ID: ")

    print("\nWhat would you like to update?")
    print("1. Price")
    print("2. Stock")

    choice = input("Choose an option: ")

    if choice == "1":
        price = float(input("Enter new price: "))
        data = {"price": price}

    elif choice == "2":
        stock = int(input("Enter new stock level: "))
        data = {"stock": stock}

    else:
        print("Invalid option.")
        return

    response = requests.patch(
        f"{BASE_URL}/inventory/{item_id}",
        json=data
    )

    if response.status_code == 200:
        print("\nItem updated successfully!")
        print(response.json())
    else:
        print("Inventory item not found.")


def delete_item():
    item_id = input("Enter inventory ID: ")

    response = requests.delete(
        f"{BASE_URL}/inventory/{item_id}"
    )

    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print("Inventory item not found.")


def find_product():
    barcode = input("Enter product barcode: ")

    response = requests.get(
        f"{BASE_URL}/products/{barcode}"
    )

    if response.status_code == 200:
        product = response.json()

        print("\nProduct found:")
        print(f"Product: {product.get('product_name')}")
        print(f"Brand: {product.get('brand')}")
        print(f"Ingredients: {product.get('ingredients_text')}")
        print(f"Barcode: {product.get('barcode')}")
    else:
        print("Product not found in OpenFoodFacts.")


def menu():
    while True:
        print("\n===== INVENTORY MANAGEMENT =====")
        print("1. View all inventory")
        print("2. View one item")
        print("3. Add item")
        print("4. Update item")
        print("5. Delete item")
        print("6. Find product on OpenFoodFacts")
        print("7. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            view_inventory()

        elif choice == "2":
            view_item()

        elif choice == "3":
            add_item()

        elif choice == "4":
            update_item()

        elif choice == "5":
            delete_item()

        elif choice == "6":
            find_product()

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    menu()