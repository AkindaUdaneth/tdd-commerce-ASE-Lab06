import pytest
from unittest.mock import Mock
from src.checkout import CheckoutService, PaymentFailedError
from src.cart import LineItem

@pytest.fixture
def mock_cart():
    cart = Mock()
    cart.items = {"LAP-001": LineItem("LAP-001", 1, 1200.0)}
    return cart

@pytest.fixture
def mock_inventory():
    inventory = Mock()
    inventory.get_available.return_value = 5
    return inventory

@pytest.fixture
def mock_discount_engine():
    engine = Mock()
    engine.calculate_total.return_value = 1140.0
    return engine

@pytest.fixture
def mock_payment_gateway():
    gateway = Mock()
    gateway.charge.return_value = True 
    return gateway

@pytest.fixture
def mock_order_repo():
    return Mock()

def test_successful_checkout_charges_payment_gateway(mock_cart, mock_inventory, mock_discount_engine, mock_payment_gateway, mock_order_repo):
    service = CheckoutService(mock_inventory, mock_discount_engine, mock_payment_gateway, mock_order_repo)
    result = service.process_checkout(mock_cart, "valid_stripe_token")
    
    assert result is True
    mock_payment_gateway.charge.assert_called_once_with(1140.0, "valid_stripe_token")

def test_checkout_fails_if_items_no_longer_available(mock_cart, mock_inventory, mock_discount_engine, mock_payment_gateway, mock_order_repo):
    mock_inventory.get_available.return_value = 0 
    service = CheckoutService(mock_inventory, mock_discount_engine, mock_payment_gateway, mock_order_repo)
    
    with pytest.raises(ValueError, match="Item LAP-001 is no longer available"):
        service.process_checkout(mock_cart, "valid_stripe_token")
        
    mock_payment_gateway.charge.assert_not_called()
    mock_order_repo.save.assert_not_called()

def test_checkout_fails_on_payment_rejection(mock_cart, mock_inventory, mock_discount_engine, mock_payment_gateway, mock_order_repo):
    mock_payment_gateway.charge.return_value = False 
    service = CheckoutService(mock_inventory, mock_discount_engine, mock_payment_gateway, mock_order_repo)
    
    with pytest.raises(PaymentFailedError, match="Payment failed: Card declined"):
        service.process_checkout(mock_cart, "declined_token")
        
    mock_order_repo.save.assert_not_called()

def test_successful_checkout_saves_order_record(mock_cart, mock_inventory, mock_discount_engine, mock_payment_gateway, mock_order_repo):
    service = CheckoutService(mock_inventory, mock_discount_engine, mock_payment_gateway, mock_order_repo)
    service.process_checkout(mock_cart, "valid_stripe_token")
    
    mock_order_repo.save.assert_called_once()
    
    saved_order = mock_order_repo.save.call_args[0][0]
    
    assert saved_order.total == 1140.0
    assert "LAP-001" in saved_order.items
    assert getattr(saved_order, 'timestamp', None) is not None