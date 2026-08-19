from unittest.mock import patch, MagicMock
import cli


def make_mock_response(status_code, json_data):
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_response.json.return_value = json_data
    return mock_response

@patch("cli.requests.request")
def test_view_inventory(mock_request, capsys):
    mock_request.return_value = make_mock_response(200, [
        {
            "id": 1,
            "product_name": "Organic Almond Milk",
            "brand": "Silk",
            "price": 5.99,
            "stock": 20,
            "barcode": "0123456789012"
        }
    ])

    cli.view_inventory()

    captured = capsys.readouterr()
    assert "Organic Almond Milk" in captured.out
    assert "Silk" in captured.out

@patch("cli.requests.request")
@patch("builtins.input")
def test_add_item(mock_input, mock_request, capsys):
    mock_input.side_effect = [
        "Test Product",   # Product name
        "Test Brand",     # Brand
        "9.99",           # Price
        "5",              # Stock
        "1111111111111"   # Barcode
    ]

    mock_request.return_value = make_mock_response(201, {
        "id": 4,
        "product_name": "Test Product",
        "brand": "Test Brand",
        "price": 9.99,
        "stock": 5,
        "barcode": "1111111111111"
    })

    cli.add_item()

    captured = capsys.readouterr()
    assert "Item added successfully" in captured.out

@patch("cli.requests.request")
@patch("builtins.input")
def test_view_item(mock_input, mock_request, capsys):
    mock_input.return_value = "1"

    mock_request.return_value = make_mock_response(200, {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brand": "Silk",
        "price": 5.99,
        "stock": 20,
        "barcode": "0123456789012"
    })

    cli.view_item()

    captured = capsys.readouterr()
    assert "Organic Almond Milk" in captured.out

@patch("cli.requests.request")
@patch("builtins.input")
def test_update_item_price(mock_input, mock_request, capsys):
    mock_input.side_effect = ["1", "1", "6.99"]  # item_id, choice "1"=price, new price

    mock_request.return_value = make_mock_response(200, {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brand": "Silk",
        "price": 6.99,
        "stock": 20,
        "barcode": "0123456789012"
    })

    cli.update_item()

    captured = capsys.readouterr()
    assert "Item updated successfully" in captured.out

@patch("cli.requests.request")
@patch("builtins.input")
def test_delete_item(mock_input, mock_request, capsys):
    mock_input.return_value = "1"

    mock_request.return_value = make_mock_response(200, {
        "message": "Inventory item deleted successfully"
    })

    cli.delete_item()

    captured = capsys.readouterr()
    assert "deleted successfully" in captured.out

@patch("cli.requests.request")
@patch("builtins.input")
def test_find_product(mock_input, mock_request, capsys):
    mock_input.return_value = "1234567890123"

    mock_request.return_value = make_mock_response(200, {
        "product_name": "Mock Cereal",
        "brand": "MockBrand",
        "ingredients_text": "Oats, sugar, salt",
        "barcode": "1234567890123"
    })

    cli.find_product()

    captured = capsys.readouterr()
    assert "Mock Cereal" in captured.out

@patch("builtins.input")
def test_get_float_reprompts_on_invalid(mock_input, capsys):
    mock_input.side_effect = ["abc", "9.99"]

    result = cli.get_float("Price: ")

    assert result == 9.99
    captured = capsys.readouterr()
    assert "Please enter a valid number" in captured.out