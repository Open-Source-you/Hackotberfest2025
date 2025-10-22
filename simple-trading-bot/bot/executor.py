class Executor:
    def __init__(self):
        self.balance = 1000
        self.position = 0

    def execute(self, decision, price):
        if decision == "buy" and self.balance >= price:
            self.position += 1
            self.balance -= price
            print(f"BUY executed at {price} | Balance: {self.balance:.2f}")
        elif decision == "sell" and self.position > 0:
            self.position -= 1
            self.balance += price
            print(f"SELL executed at {price} | Balance: {self.balance:.2f}")
        else:
            print(f"No action taken ({decision})")
