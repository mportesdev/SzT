from collections import Counter

import pytest

from szt import svet
from szt.postavy import Obchodník
from szt.utility import s_odchylkou, skupiny_kláves, okraje
from szt.veci import Věc


@pytest.fixture
def svět():
    return svet.Svět()


@pytest.mark.parametrize('x, y', ((0, 1), (-1, -1), (33, 28), (34, 27),
                                  (10, 1), (1, 10), (5, 5), (24, 13)))
def test_mistnost_na_pozici_je_none(svět, x, y):
    """Test world.Svět.místnost_na_pozici"""
    assert svět.místnost_na_pozici(x, y) is None


@pytest.mark.parametrize('x, y, typ_místnosti', ((8, 6, svet.Les),
                                                 (25, 12, svet.JeskyněBoj),
                                                 (19, 12, svet.JeskyněZbraň),
                                                 (22, 14, svet.JeskyněZlato)))
def test_mistnost_na_pozici_je_spravny_typ(svět, x, y, typ_místnosti):
    """Test world.Svět.místnost_na_pozici"""
    assert isinstance(svět.místnost_na_pozici(x, y), typ_místnosti)


@pytest.mark.parametrize('x, y, atribut', ((25, 3, 'zlato'),
                                           (25, 3, 'zlato_sebráno'),
                                           (11, 23, 'zbraň'),
                                           (11, 23, 'zbraň_sebrána'),
                                           (16, 15, 'lék'),
                                           (16, 15, 'lék_sebrán'),
                                           (9, 15, 'nepřítel')))
def test_mistnost_na_pozici_ma_specialni_atribut(svět, x, y, atribut):
    """Test world.Svět.místnost_na_pozici"""
    assert hasattr(svět.místnost_na_pozici(x, y), atribut)


@pytest.fixture
def obchodník():
    return Obchodník('', '', 0, [], ())


@pytest.mark.parametrize('cena, výsledek', ((1, 0), (2, 1),
                                            (9, 8), (10, 9), (11, 9),
                                            (99, 89), (100, 90), (101, 90),
                                            (109, 98), (110, 99), (111, 99)))
def test_vykupni_cena_obchodnika(obchodník, cena, výsledek):
    """Test npc.Obchodník.výkupní_cena"""
    věc = Věc('', cena)
    assert obchodník.výkupní_cena(věc) == výsledek


@pytest.mark.parametrize('číslo, relativní_odchylka, minimum, maximum', (
        (5, 0.2, 4, 6),     # 5 +- 1 -> [4-6]                       nůž
        (9, 0.2, 8, 10),    # 9 +- 1.8 -> [7.2-10.8] -> [8-10]      dýka
        (12, 0.2, 10, 14),  # 12 +- 2.4 -> [9.6-14.4] -> [10-14]    sekerka
        (16, 0.2, 13, 19),  # 16 +- 3.2 -> [12.8-19.2] -> [13-19]   rezavý meč
        (18, 0.2, 15, 21),  # 18 +- 3.6 -> [14.4-21.6] -> [15-21]   palcát
        (19, 0.2, 16, 22),  # 19 +- 3.8 -> [15.2-22.8] -> [16-22]   halapartna
        (20, 0.2, 16, 24),  # 20 +- 4 -> [16-24]                    řemdih
        (24, 0.2, 20, 28),  # 24 +- 4.8 -> [19.2-28.8] -> [20-28]   meč
        (26, 0.2, 21, 31),  # 26 +- 5.2 -> [20.8-31.2] -> [21-31]   těžká sekera
        (100, 0.1, 90, 110),  # 100 +- 10 -> [90-110]
        (5, 0.33, 4, 6),       # 5 +- 1.65 -> [3.35, 6.65] -> [4-6]
        (15, 0.05, 15, 15),     # 15 +- 0.75 -> [14.25-15.75] -> [15-15]
        (487, 0.26, 361, 613)  # 487 +- 126.62 -> [360.38-613.62] -> [361-613]
))
def test_s_odchylkou(číslo, relativní_odchylka, minimum, maximum):
    """Test utils.s_odchylkou"""
    výsledky = Counter(s_odchylkou(číslo, relativní_odchylka)
                       for __ in range(10_000))
    assert min(výsledky) == minimum
    assert max(výsledky) == maximum
    assert len(výsledky) == maximum - minimum + 1


@pytest.mark.parametrize('klávesy, výsledek', (
        ('BOSJZVLIK', ('BO', 'SJZV', 'LIK')),
        ('', ('', '', '')),
        ('SVIK', ('', 'SV', 'IK')),
        ('BJZLIK', ('B', 'JZ', 'LIK')),
))
def test_skupiny_klaves(klávesy, výsledek):
    """Test utils.skupiny_kláves"""
    assert skupiny_kláves(klávesy) == výsledek


@pytest.mark.parametrize('parametry, výsledek', (
        (('     H    ', ' '), (5, 4)),
        (('.  ', ' '), (0, 2)),
        (('   .', ' '), (3, 0)),
        (('......', ' '), (0, 0)),
        (('', ' '), (0, 0)),
        (('   ', ' '), (3, 0)),
        (('               ..H..                         ', ' '), (15, 25))
))
def test_okraje(parametry, výsledek):
    """Test utils.okraje"""
    assert okraje(*parametry) == výsledek
