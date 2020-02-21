from collections import Counter
import pytest

from items import Item
from npc import Trader
from utils import Color, multicolor, oscillate, hotkey_groups, okolí
import world


@pytest.fixture
def game_world():
    return world.Svět()


@pytest.mark.parametrize('x, y', ((0, 1), (-1, -1), (33, 28), (34, 27),
                                  (10, 1), (1, 10), (5, 5), (24, 13)))
def test_mistnost_na_pozici_je_none(game_world, x, y):
    """Test world.Svět.místnost_na_pozici"""
    assert game_world.místnost_na_pozici(x, y) is None


@pytest.mark.parametrize('x, y, tile_class', ((8, 6, world.Les),
                                              (25, 12, world.JeskyněBoj),
                                              (19, 12, world.JeskyněZbraň),
                                              (22, 14, world.JeskyněZlato)))
def test_mistnost_na_pozici_je_spravny_typ(game_world, x, y, tile_class):
    """Test world.Svět.místnost_na_pozici"""
    assert isinstance(game_world.místnost_na_pozici(x, y), tile_class)


@pytest.mark.parametrize('x, y, attribute', ((25, 3, 'zlato'),
                                             (25, 3, 'zlato_sebráno'),
                                             (11, 23, 'zbraň'),
                                             (11, 23, 'zbraň_sebrána'),
                                             (16, 15, 'léčivka'),
                                             (16, 15, 'léčivka_sebrána'),
                                             (9, 15, 'nepřítel')))
def test_mistnost_na_pozici_ma_specialni_atribut(game_world, x, y, attribute):
    """Test world.Svět.místnost_na_pozici"""
    assert hasattr(game_world.místnost_na_pozici(x, y), attribute)


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


@pytest.mark.parametrize('inputs, result', (
        (('     H    ', ' '), (5, 4)),
        (('.  ', ' '), (0, 2)),
        (('   .', ' '), (3, 0)),
        (('......', ' '), (0, 0)),
        (('', ' '), (0, 0)),
        (('   ', ' '), (3, 0)),
        (('               ..H..                         ', ' '), (15, 25))
))
def test_leading_trailing(inputs, result):
    assert okolí(*inputs) == result


def test_multicolor():
    multicolor('red|blue|magenta|cyan',
               (Color.RED, Color.BLUE, Color.MAGENTA, Color.CYAN))

    multicolor('Číslo položky             (|Enter| = návrat) ',
               (Color.BLUE, None))
    multicolor('Číslo položky             (|Enter| = návrat) ',
               (Color.BLUE, None, Color.BLUE),
               repeat=False)

    multicolor('K|: koupit    |P|: prodat    (|Enter| = návrat) ',
               (None, Color.BLUE))
    multicolor('K|: koupit    |P|: prodat    (|Enter| = návrat) ',
               (None, Color.BLUE, None, Color.BLUE, None, Color.BLUE),
               repeat=False)

    multicolor('[ |+| les           |#| jeskyně         '
               '|H| hráč            |?| neznámo ]',
               (Color.BLUE, None))
    multicolor('[ |+| les           |#| jeskyně         '
               '|H| hráč            |?| neznámo ]',
               (Color.BLUE, None, Color.BLUE, None, Color.BLUE, None,
                Color.BLUE, None, Color.BLUE),
               repeat=False)

    multicolor(f'[ Zdraví: |{64:<8}|zkušenost: |{1024:<7}|zlato: |128| ]',
               (Color.MAGENTA, None))
    multicolor(f'[ Zdraví: |{64:<8}|zkušenost: |{1024:<7}|zlato: |128| ]',
               (Color.MAGENTA, None, Color.MAGENTA, None, Color.MAGENTA, None,
                Color.MAGENTA),
               repeat=False)

    with pytest.raises(ValueError):
        multicolor('Číslo položky             (|Enter| = návrat) ',
                   (Color.BLUE, None),
                   repeat=False)

    with pytest.raises(ValueError):
        multicolor('K|: koupit    |P|: prodat    (|Enter| = návrat) ',
                   (None, Color.BLUE, None, Color.BLUE, None),
                   repeat=False)

    with pytest.raises(ValueError):
        multicolor('[ |+| les           |#| jeskyně         '
                   '|H| hráč            |?| neznámo ]',
                   (Color.BLUE, None, Color.BLUE, None, Color.BLUE, None,
                    Color.BLUE, None),
                   repeat=False)

    with pytest.raises(ValueError):
        multicolor(f'[ Zdraví: |{64:<8}|zkušenost: |{1024:<7}|zlato: |128| ]',
                   (Color.MAGENTA, None, Color.MAGENTA, None, Color.MAGENTA,
                    None),
                   repeat=False)
