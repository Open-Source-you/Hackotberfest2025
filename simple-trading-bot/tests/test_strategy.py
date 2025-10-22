from bot.strategy import placeholder_strategy


def test_placeholder_strategy_buy():
    assert placeholder_strategy(99) == "buy"


def test_placeholder_strategy_sell():
    assert placeholder_strategy(102) == "sell"


def test_placeholder_strategy_none():
    assert placeholder_strategy(100.5) is None
