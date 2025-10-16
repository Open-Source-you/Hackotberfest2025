"""
CoinGecko Market Data Adapter

Fetches public market data from CoinGecko API with rate-limit handling.
Integration is optional and safe if not configured.
"""
import requests
import time

class CoinGeckoAdapter:
    BASE_URL = "https://api.coingecko.com/api/v3"
    RATE_LIMIT_SLEEP = 2  # seconds to wait on rate limit

    def __init__(self, enabled=True):
        self.enabled = enabled

    def fetch_price(self, coin_id="bitcoin", vs_currency="usd"):
        if not self.enabled:
            print("CoinGecko integration is disabled.")
            return None
        url = f"{self.BASE_URL}/simple/price"
        params = {"ids": coin_id, "vs_currencies": vs_currency}
        for attempt in range(3):
            try:
                response = requests.get(url, params=params)
                if response.status_code == 429:
                    print("Rate limit hit. Retrying...")
                    time.sleep(self.RATE_LIMIT_SLEEP)
                    continue
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                print(f"Error fetching price: {e}")
                time.sleep(self.RATE_LIMIT_SLEEP)
        return None

if __name__ == "__main__":
    adapter = CoinGeckoAdapter(enabled=True)
    price = adapter.fetch_price("bitcoin", "usd")
    print("Bitcoin price:", price)
