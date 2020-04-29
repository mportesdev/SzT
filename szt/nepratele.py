# coding: utf-8

import random

from . import data, veci


class Nepřítel:
    def __init__(já, jméno, zdraví, útok,
                 jméno_3_pád=None, jméno_4_pád=None,
                 text_živý=None, text_mrtvý=None):
        já.jméno = jméno
        já.krátké_jméno = já.jméno.split()[-1].lower()
        já.zdraví = zdraví
        já.útok = útok

        já.jméno_3_pád = jméno_3_pád or já.jméno
        já.jméno_4_pád = jméno_4_pád or já.jméno

        já.text_živý = text_živý or f'Zaútočil na tebe {já.jméno.lower()}!'
        já.text_mrtvý = text_mrtvý or ('Na zemi leží mrtvý'
                                       f' {já.jméno.lower()}.')

    def __str__(já):
        return já.jméno

    def žije(já):
        return já.zdraví > 0

    @property
    def text(já):
        return já.text_živý if já.žije() else já.text_mrtvý


class Zvíře(Nepřítel):
    pass


class Netvor(Nepřítel):
    def __init__(já, jméno, zdraví, útok,
                 jméno_3_pád=None, jméno_4_pád=None,
                 text_živý=None, text_mrtvý=None):
        super().__init__(jméno, zdraví, útok,
                         jméno_3_pád, jméno_4_pád, text_živý, text_mrtvý)
        já.zlato = random.randint(8, 16)
        já.zlato_sebráno = False

    @classmethod
    def troll(třída):
        return třída(**data.parametry_troll)

    @classmethod
    def lesní_troll(třída):
        return třída(**data.parametry_lesní_troll)


class Člověk(Nepřítel):
    def __init__(já, jméno, zdraví, zbraň,
                 jméno_3_pád=None, jméno_4_pád=None,
                 text_živý=None, text_mrtvý=None):
        já.zbraň = zbraň
        super().__init__(jméno, zdraví, já.zbraň.útok,
                         jméno_3_pád, jméno_4_pád, text_živý, text_mrtvý)
        já.zbraň_sebrána = False
        já.zlato = random.choice((0, random.randint(10, 20)))
        já.zlato_sebráno = False

    @classmethod
    def dobrodruh(třída):
        return třída(**data.parametry_dobrodruh,
                     zbraň=veci.Zbraň(*data.zbraň_dobrodruh))


def náhodný_jeskynní_nepřítel():
    název_třídy, parametry = random.choice(data.data_nepřátel[:6])
    třída = {'zvíře': Zvíře,
             'netvor': Netvor,
             'člověk': Člověk}.get(název_třídy)
    return třída(**parametry)


def náhodný_lesní_nepřítel():
    název_třídy, parametry = random.choice(data.data_nepřátel[6:])
    třída = {'zvíře': Zvíře,
             'netvor': Netvor,
             'člověk': Člověk}.get(název_třídy)
    return třída(**parametry)
