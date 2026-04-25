"""Sprint 6: Shoe Order class.

This module defines a simple ShoeOrder class for the shoe store
sales tracker. It stores the salesperson and shoe details and
provides methods to update values and display the order.
"""

class ShoeOrder:
    """A class that holds a shoe order for the store."""

    def __init__(self, salesperson, brand, model, size, price):
        self.salesperson = salesperson
        self.brand = brand
        self.model = model
        self.size = size
        self.price = price

    def set_brand(self, brand):
        """Update the shoe brand."""
        self.brand = brand

    def set_model(self, model):
        """Update the shoe model."""
        self.model = model

    def set_size(self, size):
        """Update the shoe size."""
        self.size = size

    def set_price(self, price):
        """Update the shoe price."""
        self.price = price

    def display_order(self):
        """Print the order details with numbered output."""
        print("Shoe Order Details:")
        print("1. Salesperson: {}".format(self.salesperson))
        print("2. Brand: {}".format(self.brand))
        print("3. Model: {}".format(self.model))
        print("4. Size: {}".format(self.size))
        print("5. Price: ${:.2f}".format(self.price))
