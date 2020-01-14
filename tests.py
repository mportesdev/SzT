import pytest

from items import Item
from npc import Trader


@pytest.fixture
def trader():
    return Trader('name', 'text', 0, [], ())


@pytest.fixture
def item():
    return Item('name', 100)


@pytest.mark.parametrize('value, result', ((1, 0), (2, 1),
                                           (9, 8), (10, 9), (11, 9),
                                           (99, 89), (100, 90), (101, 90),
                                           (109, 98), (110, 99), (111, 99)))
def test_trader_buy_price(trader, item, value, result):
    item.value = value
    assert trader.buy_price(item) == result
