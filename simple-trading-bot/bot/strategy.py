def placeholder_strategy(price):
    if price < 100:
        return "buy"
    elif price > 101:
        return "sell"
    return None
