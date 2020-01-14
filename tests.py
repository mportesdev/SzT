from collections import Counter
import pytest

from items import Item
from npc import Trader
from utils import oscillate


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
    """Test npc.Trader.buy_price"""
    item.value = value
    assert trader.buy_price(item) == result


@pytest.mark.parametrize('n, relative_delta, expected_min, expected_max', (
        (100, 0.1, 90, 110),  # 100 +- 10 -> [90-110]
        (5, 0.33, 4, 6),       # 5 +- 1.65 -> [3.35, 6.65] -> [4-6]
        (15, 0.05, 15, 15),     # 15 +- 0.75 -> [14.25-15.75] -> [15-15]
        (487, 0.26, 361, 613)  # 487 +- 126.62 -> [360.38-613.62] -> [361-613]
))
def test_oscillate(n, relative_delta, expected_min, expected_max):
    """Test utils.oscillate"""
    results = Counter(oscillate(n, relative_delta) for __ in range(10_000))
    assert min(results) == expected_min
    assert max(results) == expected_max
    assert len(results) == expected_max - expected_min + 1
