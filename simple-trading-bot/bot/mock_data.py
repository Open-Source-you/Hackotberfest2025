import random


class MockMarket:
    def __init__(self, base_price=100.0):
        self.price = base_price

    def get_price(self):
        self.price *= random.uniform(0.99, 1.01)
        return round(self.price, 2)
