from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Protocol
from src.cart import LineItem

@dataclass
class Order:
    items: Dict[str, LineItem]
    total: float
    timestamp: datetime = field(default_factory=datetime.now)

class OrderRepository(Protocol):
    """Protocol defining how orders are saved to the database."""
    def save(self, order: Order) -> None:
        ...