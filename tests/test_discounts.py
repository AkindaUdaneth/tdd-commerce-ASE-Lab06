# tests/test_discounts.py
import pytest
from unittest.mock import Mock
from src.discount import DiscountEngine
from src.cart import LineItem

@pytest.fixture
def mock_cart():
    return Mock()

def test_bulk_discount_applies_10_percent_off_line(mock_cart):
    mock_cart.items = {"MOU-001": LineItem("MOU-001", 10, 15.0)}
    mock_cart.calculate_total.return_value = 150.0
    
    engine = DiscountEngine()
    assert engine.calculate_total(mock_cart) == 135.0
    
def test_order_discount_applies_5_percent_off_totals_over_1000(mock_cart):
    mock_cart.items = {"LAP-001": LineItem("LAP-001", 1, 1200.0)}
    mock_cart.calculate_total.return_value = 1200.0
    
    engine = DiscountEngine()
    assert engine.calculate_total(mock_cart) == 1140.0
    
def test_both_discounts_apply_in_sequence(mock_cart):
    mock_cart.items = {"MON-001": LineItem("MON-001", 10, 200.0)}
    mock_cart.calculate_total.return_value = 2000.0
    
    engine = DiscountEngine()
    assert engine.calculate_total(mock_cart) == 1710.0
    
def test_no_discount_applied_for_small_orders(mock_cart):
    mock_cart.items = {"KEY-001": LineItem("KEY-001", 5, 100.0)}
    mock_cart.calculate_total.return_value = 500.0
    
    engine = DiscountEngine()
    assert engine.calculate_total(mock_cart) == 500.0