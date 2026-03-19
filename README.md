# TDD E-Commerce Platform

A lightweight e-commerce backend built entirely using **Test-Driven Development (TDD)**. This project demonstrates the strict application of the **Red ➔ Green ➔ Refactor** cycle using Python and `pytest`.

---

## 🚀 Features

This project was built incrementally, fulfilling the following architectural requirements:

* **Requirement A - Catalog & Products:** Immutable product models and a searchable catalog.
* **Requirement B - Shopping Cart:** Line item management and dynamic total calculation.
* **Requirement C - Inventory Reservation:** Dependency injection of an `InventoryGateway` to simulate stock validation.
* **Requirement D - Discount Engine:** Implementation of the Strategy Pattern to apply pluggable bulk and order-level discounts.
* **Requirement E - Checkout Orchestration:** A `CheckoutService` that coordinates inventory, discounts, and a mocked `PaymentGateway`.
* **Requirement F - Order Persistence:** Generation of immutable `Order` records saved to a mocked `OrderRepository` upon successful payment.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Testing Framework:** `pytest`
* **Techniques Used:** Mocking (`unittest.mock`), Dependency Injection, Strategy Pattern, Dataclasses (Value Objects), Type Hinting.

---

## 📂 Project Structure

```text
tdd-ecommerce/
│
├── src/                  # Application source code
│   ├── cart.py           # Cart and LineItem models
│   ├── catalog.py        # Product and Catalog models
│   ├── checkout.py       # Checkout orchestration service
│   ├── discount.py       # Discount rules and engine
│   ├── inventory.py      # Inventory interfaces
│   └── order.py          # Order models and repository interfaces
│
├── tests/                # Unit tests
│   ├── test_cart.py
│   ├── test_catalog.py
│   ├── test_checkout.py
│   └── test_discounts.py
│
├── pytest.ini            # Pytest configuration
└── requirements.txt      # Project dependencies
```

---

## 💻 Local Setup & Testing

To run this project locally, clone the repository and set up a virtual environment.

```bash
# Clone the repository
git clone [https://github.com/AkindaUdaneth/tdd-commerce-ASE-Lab06.git](https://github.com/AkindaUdaneth/tdd-commerce-ASE-Lab06.git)
cd tdd-ecommerce-lab

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Run the test suite
pytest
```
