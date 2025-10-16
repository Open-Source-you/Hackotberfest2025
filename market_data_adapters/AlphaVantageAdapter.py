"""
Alpha Vantage Market Data Adapter

Fetches public market data from Alpha Vantage API with rate-limit handling.
Integration is optional and safe if no API key is provided.

How to obtain an API key:
- Visit https://www.alphavantage.co/support/#api-key
- Sign up for a free API key.

How to configure:
- Set the environment variable ALPHAVANTAGE_API_KEY with your API key.
- Or pass the API key directly to the adapter.
"""
import os
import requests
import time

class AlphaVantageAdapter:
    BASE_URL = "https://www.alphavantage.co/query"
    RATE_LIMIT_SLEEP = 15  # seconds to wait on rate limit

    def __init__(self, api_key=None, enabled=True):
        self.api_key = api_key or os.getenv("ALPHAVANTAGE_API_KEY")
        self.enabled = enabled and bool(self.api_key)

    def fetch_price(self, symbol="IBM"):
        if not self.enabled:
            print("Alpha Vantage integration is disabled or API key missing.")
            return None
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": self.api_key
        }
        for attempt in range(3):
            try:
                response = requests.get(self.BASE_URL, params=params)
                if response.status_code == 429:
                    print("Rate limit hit. Retrying...")
                    time.sleep(self.RATE_LIMIT_SLEEP)
                    continue
                response.raise_for_status()
                data = response.json()
                return data.get("Global Quote", {})
            except requests.RequestException as e:
                print(f"Error fetching price: {e}")
                time.sleep(self.RATE_LIMIT_SLEEP)
        return None

if __name__ == "__main__":
    # Example usage
    adapter = AlphaVantageAdapter()
    price = adapter.fetch_price("IBM")
    print("IBM price:", price)
