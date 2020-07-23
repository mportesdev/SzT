# coding: utf-8

import math
import random
import re

from . import data


def s_odchylkou(číslo, relativní_odchylka=0.2):
    odchylka = int(číslo * relativní_odchylka)
    return random.randint(číslo - odchylka, číslo + odchylka)


def výkupní_cena(cena, marže):
    return cena * 100 // (100 + marže)


def okraje(řetězec, hodnota_okraje):
    vzorec = f'^({hodnota_okraje}*).*?({hodnota_okraje}*)$'
    levý_okraj, pravý_okraj = re.match(vzorec, řetězec).groups()

    return len(levý_okraj), len(pravý_okraj)


def text_místnosti_ze_souřadnic(typ_zón, x, y):
    vzdálenost_od_středu = math.hypot(x - 18, y - 10)

    if typ_zón == 'jeskyně':
        zóna = min(int(vzdálenost_od_středu / 3), 5)
        return data.texty_jeskyně[zóna]

    zóna = int(vzdálenost_od_středu / 3) // 2
    return data.texty_les[zóna]
