from typing import Protocol
from src.cart import Cart
from src.inventory import InventoryGateway
from src.discount import DiscountEngine
from src.order import Order, OrderRepository

class PaymentGateway(Protocol):
    def charge(self, amount: float, token: str) -> bool:
        ...

class PaymentFailedError(Exception):
    pass

class CheckoutService:
    def __init__(self, inventory: InventoryGateway, 
                 discount_engine: DiscountEngine, 
                 payment_gateway: PaymentGateway, 
                 order_repo: OrderRepository):
        self._inventory = inventory
        self._discount_engine = discount_engine
        self._payment_gateway = payment_gateway
        self._order_repo = order_repo

    def process_checkout(self, cart: Cart, payment_token: str) -> bool:
        self._validate_inventory(cart)
        final_total = self._discount_engine.calculate_total(cart)
        
        if not self._payment_gateway.charge(final_total, payment_token):
            raise PaymentFailedError("Payment failed: Card declined")

        order = Order(cart.items, final_total)
        self._order_repo.save(order)

        return True

    def _validate_inventory(self, cart: Cart) -> None:
        for sku, item in cart.items.items():
            if self._inventory.get_available(sku) < item.quantity:
                raise ValueError(f"Item {sku} is no longer available")