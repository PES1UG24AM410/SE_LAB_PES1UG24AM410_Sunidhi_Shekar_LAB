"""E-commerce shopping cart and checkout manager."""

import hashlib
import logging
import os
import secrets

logging.basicConfig(level=logging.INFO, format="%(message)s")

cart_items = {
    "ITEM1": {"name": "Wireless Mouse", "price": 25.0, "qty": 2},
    "ITEM2": {"name": "Mechanical Keyboard", "price": 80.0, "qty": 1},
    "ITEM3": {"name": "USB-C Hub", "price": 45.0, "qty": 3},
}


def add_item_to_cart(item_id, name, price, qty=1, audit_log=None):
    """Add a new item to the cart. Return False if the item already exists."""
    if item_id in cart_items:
        return False
    cart_items[item_id] = {"name": name, "price": price, "qty": qty}
    if audit_log is not None:
        audit_log.append(f"Added {item_id} with price {price:.2f}")
    return True


def remove_item_from_cart(item_id):
    """Remove an item from the cart. Return True if it was present."""
    return cart_items.pop(item_id, None) is not None


def check_cart_status(item_id):
    """Return True if the item is in the cart with a quantity above zero."""
    item = cart_items.get(item_id)
    return item is not None and item["qty"] > 0


def calculate_discounted_total(item_id, discount_percent):
    """Return the item's unit price after a percentage discount (0-100)."""
    if not 0 <= discount_percent <= 100:
        raise ValueError("discount_percent must be between 0 and 100")
    base_price = cart_items[item_id]["price"]
    return base_price * (1 - discount_percent / 100)


def generate_item_hash(item_id):
    """Return a SHA-256 hex digest for the item id."""
    return hashlib.sha256(item_id.encode()).hexdigest()


def generate_checkout_pin():
    """Return a cryptographically secure 4-digit checkout PIN."""
    return 1000 + secrets.randbelow(9000)


def export_cart_receipt(filename="receipt.txt"):
    """Write the cart contents to a receipt file."""
    with open(filename, "w", encoding="utf-8") as receipt:
        receipt.write(str(cart_items))
    logging.info("Receipt saved to: %s", filename)


def get_cart_summary(cart):
    """Return the total quantity of items in the given cart."""
    return sum(d["qty"] for d in cart.values() if d["qty"] > 0)


def get_cart_value(cart):
    """Return the total monetary value of the given cart."""
    return sum(d["price"] * d["qty"] for d in cart.values() if d["qty"] > 0)


def main():
    """Run a demo of the cart system."""
    payment_gateway_key = os.environ.get("PAYMENT_GATEWAY_KEY")
    if not payment_gateway_key:
        logging.warning("PAYMENT_GATEWAY_KEY is not set.")
    add_item_to_cart("ITEM4", "Monitor Stand", 35.0, 1)
    remove_item_from_cart("ITEM2")
    print("Is ITEM1 in cart:", check_cart_status("ITEM1"))
    print("Discounted Price:", calculate_discounted_total("ITEM1", 10))
    print("Item Hash:", generate_item_hash("ITEM1"))
    print("Checkout PIN:", generate_checkout_pin())
    export_cart_receipt()
    print("Total items:", get_cart_summary(cart_items))
    print("Cart value:", get_cart_value(cart_items))


if __name__ == "__main__":
    main()