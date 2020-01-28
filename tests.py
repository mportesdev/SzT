from collections import Counter
import pytest

from items import Item
from npc import Trader
from utils import oscillate, hotkey_groups
import world


@pytest.fixture
def game_world():
    return world.World()


@pytest.mark.parametrize('x, y', ((0, 0), (-1, -1), (33, 28), (34, 27),
                                  (10, 1), (1, 10), (5, 5), (24, 13)))
def test_world_tile_at_returns_none(game_world, x, y):
    """Test world.World.tile_at"""
    assert game_world.tile_at(x, y) is None


@pytest.mark.parametrize('x, y, tile_class', ((8, 6, world.Forest),
                                              (25, 12, world.CaveWithEnemy),
                                              (15, 8, world.CaveWithWeapon),
                                              (22, 14, world.FindGoldTile)))
def test_world_tile_at_returns_correct_tile(game_world, x, y, tile_class):
    """Test world.World.tile_at"""
    assert isinstance(game_world.tile_at(x, y), tile_class)


@pytest.mark.parametrize('x, y, attribute', ((25, 3, 'gold'),
                                             (25, 3, 'gold_claimed'),
                                             (11, 23, 'weapon'),
                                             (11, 23, 'weapon_claimed'),
                                             (16, 15, 'consumable'),
                                             (16, 15, 'consumable_claimed'),
                                             (9, 15, 'enemy')))
def test_special_tiles_attribute(game_world, x, y, attribute):
    """Test world.World.tile_at"""
    assert hasattr(game_world.tile_at(x, y), attribute)


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
        (5, 0.2, 4, 6),     # 5 +- 1 -> [4-6]                       knife
        (9, 0.2, 8, 10),    # 9 +- 1.8 -> [7.2-10.8] -> [8-10]      dagger
        (12, 0.2, 10, 14),  # 12 +- 2.4 -> [9.6-14.4] -> [10-14]    hatchet
        (16, 0.2, 13, 19),  # 16 +- 3.2 -> [12.8-19.2] -> [13-19]   rusty sword
        (18, 0.2, 15, 21),  # 18 +- 3.6 -> [14.4-21.6] -> [15-21]   mace
        (19, 0.2, 16, 22),  # 19 +- 3.8 -> [15.2-22.8] -> [16-22]   halberd
        (20, 0.2, 16, 24),  # 20 +- 4 -> [16-24]                    morning star
        (24, 0.2, 20, 28),  # 24 +- 4.8 -> [19.2-28.8] -> [20-28]   sword
        (26, 0.2, 21, 31),  # 26 +- 5.2 -> [20.8-31.2] -> [21-31]   heavy axe
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


@pytest.mark.parametrize('hotkeys, result', (
        ('BOSJZVLIK', ('BO', 'SJZV', 'LIK')),
        ('', ('', '', '')),
        ('SVIK', ('', 'SV', 'IK')),
        ('BJZLIK', ('B', 'JZ', 'LIK')),
))
def test_hotkey_groups(hotkeys, result):
    assert hotkey_groups(hotkeys) == result
