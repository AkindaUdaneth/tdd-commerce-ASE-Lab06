from typing import Protocol, List
from src.cart import Cart

class DiscountRule(Protocol):
    """Protocol for all discount strategies."""
    def apply(self, cart: Cart, current_total: float) -> float:
        ...

class BulkDiscountRule:
    def apply(self, cart: Cart, current_total: float) -> float:
        discount = 0.0
        for item in cart.items.values():
            if item.quantity >= 10:
                discount += (item.price * item.quantity) * 0.10
        return current_total - discount

class OrderDiscountRule:
    def apply(self, cart: Cart, current_total: float) -> float:
        if current_total >= 1000.0:
            return current_total * 0.95
        return current_total

class DiscountEngine:
    def __init__(self, rules: List[DiscountRule] = None):
        self.rules = rules if rules is not None else [BulkDiscountRule(), OrderDiscountRule()]

    def calculate_total(self, cart: Cart) -> float:
        total = cart.calculate_total()
        for rule in self.rules:
            total = rule.apply(cart, total)
        return total