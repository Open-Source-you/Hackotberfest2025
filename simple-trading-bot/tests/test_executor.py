from bot.executor import Executor


def test_execute_buy():
    e = Executor()
    e.execute("buy", 100)
    assert e.balance < 1000
    assert e.position == 1


def test_execute_sell():
    e = Executor()
    e.position = 1
    e.execute("sell", 101)
    assert e.balance > 1000
