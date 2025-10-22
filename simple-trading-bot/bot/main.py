import time

from .config import load_config
from .executor import Executor
from .mock_data import MockMarket
from .strategy import placeholder_strategy


def main():
    config = load_config()
    market = MockMarket()
    executor = Executor()

    print("Starting trading bot with mock data...")
    for _ in range(config["iterations"]):
        price = market.get_price()
        decision = placeholder_strategy(price)
        if decision:
            executor.execute(decision, price)
        time.sleep(config["interval"])

    print("\nBot finished running.")
    print("--- Final Summary ---")
    print(f"Final Balance: {executor.balance:.2f}")
    print(f"Final Position (units held): {executor.position}")
    total_value = executor.balance + executor.position * market.price
    profit_loss = total_value - config["starting_balance"]
    print(f"Total Profit/Loss: {profit_loss:.2f}")


if __name__ == "__main__":
    main()
