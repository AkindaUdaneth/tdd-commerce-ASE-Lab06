import pytest
from src.catalog import Product, Catalog

def test_product_creation_valid_attributes():
    product = Product(sku="LAP-001", name="Gaming Laptop", price=1200.0)
    assert product.sku == "LAP-001"
    assert product.name == "Gaming Laptop"
    assert product.price == 1200.0

def test_product_rejects_negative_price():
    with pytest.raises(ValueError, match="Price cannot be negative"):
        Product(sku="MOU-001", name="Wireless Mouse", price=-15.0)

def test_catalog_adds_and_retrieves_product():
    catalog = Catalog()
    product = Product(sku="LAP-001", name="Gaming Laptop", price=1200.0)
    catalog.add_product(product)
    
    retrieved = catalog.get_product("LAP-001")
    assert retrieved == product

def test_catalog_returns_none_for_missing_sku():
    catalog = Catalog()
    retrieved = catalog.get_product("NON-EXISTENT-SKU")
    assert retrieved is None