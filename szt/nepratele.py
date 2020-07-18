# coding: utf-8

import random
import sys

from . import data, veci

tento_modul = sys.modules[__name__]


class Nepřítel:
    def __init__(self, jméno, zdraví, útok,
                 jméno_3_pád=None, jméno_4_pád=None,
                 text_živý=None, text_mrtvý=None):
        self.jméno = jméno
        self.krátké_jméno = self.jméno.split()[-1].lower()
        self.zdraví = zdraví
        self.útok = útok

        self.jméno_3_pád = jméno_3_pád or self.jméno
        self.jméno_4_pád = jméno_4_pád or self.jméno

        self.text_živý = text_živý or f'Zaútočil na tebe {self.jméno.lower()}!'
        self.text_mrtvý = text_mrtvý or ('Na zemi leží mrtvý'
                                         f' {self.jméno.lower()}.')

    def __str__(self):
        return self.jméno

    def žije(self):
        return self.zdraví > 0

    @property
    def text(self):
        return self.text_živý if self.žije() else self.text_mrtvý


class Zvíře(Nepřítel):
    pass


class Netvor(Nepřítel):
    def __init__(self, jméno, zdraví, útok,
                 jméno_3_pád=None, jméno_4_pád=None,
                 text_živý=None, text_mrtvý=None):
        super().__init__(jméno, zdraví, útok,
                         jméno_3_pád, jméno_4_pád, text_živý, text_mrtvý)
        self.zlato = random.randint(8, 16)
        self.zlato_sebráno = False

    @classmethod
    def troll(cls):
        return cls(**data.parametry_troll)

    @classmethod
    def lesní_troll(cls):
        return cls(**data.parametry_lesní_troll)


class Člověk(Nepřítel):
    def __init__(self, jméno, zdraví, zbraň,
                 jméno_3_pád=None, jméno_4_pád=None,
                 text_živý=None, text_mrtvý=None):
        self.zbraň = zbraň
        super().__init__(jméno, zdraví, self.zbraň.útok,
                         jméno_3_pád, jméno_4_pád, text_živý, text_mrtvý)
        self.zbraň_sebrána = False
        self.zlato = random.choice((0, random.randint(10, 20)))
        self.zlato_sebráno = False

    @classmethod
    def dobrodruh(cls):
        return cls(**data.parametry_dobrodruh,
                   zbraň=veci.Zbraň(*data.zbraň_dobrodruh))


def náhodný_jeskynní_nepřítel():
    název_třídy, parametry = random.choice(data.data_nepřátel[:6])
    třída = getattr(tento_modul, název_třídy)
    return třída(**parametry)


def náhodný_lesní_nepřítel():
    název_třídy, parametry = random.choice(data.data_nepřátel[6:])
    třída = getattr(tento_modul, název_třídy)
    return třída(**parametry)
