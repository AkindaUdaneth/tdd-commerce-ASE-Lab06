from typing import Protocol

class InventoryGateway(Protocol):
    """
    Protocol defines the interface for the inventory service.
    Any class passed to Cart must implement get_available(sku).
    """
    def get_available(self, sku: str) -> int:
        ...