from dataclasses import dataclass
from typing import Dict
from src.inventory import InventoryGateway

@dataclass
class LineItem:
    sku: str
    quantity: int
    price: float

class Cart:
    def __init__(self, catalog, inventory: InventoryGateway):
        self._catalog = catalog
        self._inventory = inventory
        self._items: Dict[str, LineItem] = {}

    def add_item(self, sku: str, quantity: int) -> None:
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be an integer > 0")
            
        product = self._catalog.get_product(sku)
        if not product:
            raise ValueError("Product not found in catalog")

        available = self._inventory.get_available(sku)
        current_qty = self._items[sku].quantity if sku in self._items else 0
        
        if current_qty + quantity > available:
            raise ValueError(f"Insufficient inventory for {sku}")
            
        if sku in self._items:
            self._items[sku].quantity += quantity
        else:
            self._items[sku] = LineItem(sku, quantity, product.price)

    def remove_item(self, sku: str) -> None:
        self._items.pop(sku, None) 

    def calculate_total(self) -> float:
        return sum(item.price * item.quantity for item in self._items.values())
        
    @property
    def items(self) -> dict:
        return self._items