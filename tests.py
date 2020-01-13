import pytest

from items import Item
from npc import Trader


@pytest.fixture
def trader():
    return Trader('name', 'text', 0, [], ())


@pytest.fixture
def item():
    return Item('name', 100)


def test_trader_buy_price(trader, item):
    assert trader.buy_price(item) == 90

    item.value = 2
    assert trader.buy_price(item) == 1

    item.value = 12
    assert trader.buy_price(item) == 10
