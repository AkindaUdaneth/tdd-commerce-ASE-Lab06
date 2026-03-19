import pytest
from unittest.mock import Mock
from src.cart import Cart, LineItem

@pytest.fixture
def mock_catalog():
    catalog = Mock()
    mock_product = Mock()
    mock_product.price = 100.0
    catalog.get_product.return_value = mock_product
    return catalog

@pytest.fixture
def mock_inventory():
    inventory = Mock()
    inventory.get_available.return_value = 10
    return inventory


def test_cart_adds_valid_item(mock_catalog, mock_inventory):
    cart = Cart(catalog=mock_catalog, inventory=mock_inventory)
    cart.add_item("LAP-001", 1)
    assert "LAP-001" in cart.items

def test_cart_rejects_missing_product(mock_catalog, mock_inventory):
    mock_catalog.get_product.return_value = None
    cart = Cart(catalog=mock_catalog, inventory=mock_inventory)
    with pytest.raises(ValueError, match="Product not found in catalog"):
        cart.add_item("INVALID-SKU", 1)

def test_cart_rejects_invalid_quantity(mock_catalog, mock_inventory):
    cart = Cart(catalog=mock_catalog, inventory=mock_inventory)
    with pytest.raises(ValueError, match="Quantity must be an integer > 0"):
        cart.add_item("LAP-001", 0)

def test_cart_removes_item(mock_catalog, mock_inventory):
    cart = Cart(catalog=mock_catalog, inventory=mock_inventory)
    cart.add_item("LAP-001", 1)
    cart.remove_item("LAP-001")
    assert "LAP-001" not in cart.items

def test_cart_calculates_total(mock_catalog, mock_inventory):
    cart = Cart(catalog=mock_catalog, inventory=mock_inventory)
    cart.add_item("LAP-001", 2)
    cart.add_item("MOU-001", 3)
    assert cart.calculate_total() == 500.0


def test_cart_adds_item_when_inventory_sufficient(mock_catalog, mock_inventory):
    mock_inventory.get_available.return_value = 5
    cart = Cart(catalog=mock_catalog, inventory=mock_inventory)
    cart.add_item("LAP-001", 2)
    assert cart.items["LAP-001"].quantity == 2

def test_cart_rejects_item_when_inventory_insufficient(mock_catalog, mock_inventory):
    mock_inventory.get_available.return_value = 1
    cart = Cart(catalog=mock_catalog, inventory=mock_inventory)
    with pytest.raises(ValueError, match="Insufficient inventory for LAP-001"):
        cart.add_item("LAP-001", 2)