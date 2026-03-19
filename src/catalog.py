# src/catalog.py (Refactored)
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Price:
    amount: float
    
    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Price cannot be negative")

class Product:
    def __init__(self, sku: str, name: str, price: float):
        self.sku = sku
        self.name = name
        self._price = Price(price)
        
    @property
    def price(self) -> float:
        return self._price.amount

class Catalog:
    def __init__(self):
        self._products: dict[str, Product] = {}

    def add_product(self, product: Product) -> None:
        self._products[product.sku] = product

    def get_product(self, sku: str) -> Optional[Product]:
        return self._products.get(sku)