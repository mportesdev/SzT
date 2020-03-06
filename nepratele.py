# coding: utf-8

import random

import veci


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
        return třída(
            jméno='Kamenný troll',
            zdraví=92,
            útok=16,
            jméno_3_pád='Trollovi',
            jméno_4_pád='Trolla',
            text_živý='Vyrušil jsi dřímajícího kamenného trolla!',
            text_mrtvý='Zabitý kamenný troll připomíná obyčejnou skálu.'
        )

    @classmethod
    def lesní_troll(třída):
        return třída(
            jméno='Lesní troll',
            zdraví=62,
            útok=12,
            jméno_3_pád='Trollovi',
            jméno_4_pád='Trolla',
            text_živý='Cestu ti zastoupil mohutný troll obrostlý'
                      ' mechem.'
        )


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
        return třída(
            jméno='Cizí dobrodruh',
            zdraví=98,
            zbraň=veci.Zbraň('Železné kopí', 18, 85),
            jméno_3_pád='Dobrodruhovi',
            jméno_4_pád='Dobrodruha',
            text_živý='Vrhl se na tebe pološílený dobrodruh - jiný hráč'
                      ' této hry!',
            text_mrtvý='Na zemi leží mrtvola muže s vytřeštěnýma očima.'
        )


data_nepřátel = (
    (
        Zvíře,
        {
            'jméno': 'Obří pavouk',
            'zdraví': 29,
            'útok': 7,
            'jméno_3_pád': 'Pavoukovi',
            'jméno_4_pád': 'Pavouka',
            'text_živý': 'Z výšky se spustil obří pavouk a snaží se tě pozřít!',
            'text_mrtvý': 'Na zemi se povalují nohy a trup gigantického'
                          ' pavouka.',
        },
    ),

    (
        Zvíře,
        {
            'jméno': 'Obří šváb',
            'zdraví': 33,
            'útok': 5,
            'jméno_3_pád': 'Švábovi',
            'jméno_4_pád': 'Švába',
            'text_živý': 'Z díry vylezl odporný obří šváb a sevřel tě kusadly!',
            'text_mrtvý': 'Na zemi leží ohavná tlející mrtvola švába.',
        },
    ),

    (
        Zvíře,
        {
            'jméno': 'Obří netopýr',
            'zdraví': 36,
            'útok': 6,
            'jméno_3_pád': 'Netopýrovi',
            'jméno_4_pád': 'Netopýra',
            'text_mrtvý': 'Na zemi leží odpudivý mrtvý netopýr s polámanými'
                          ' kožnatými křídly.',
        },
    ),

    (
        Netvor,
        {
            'jméno': 'Skřet',
            'zdraví': 43,
            'útok': 12,
            'jméno_3_pád': 'Skřetovi',
            'jméno_4_pád': 'Skřeta',
        },
    ),

    (
        Netvor,
        {
            'jméno': 'Krysodlak',
            'zdraví': 47,
            'útok': 10,
            'jméno_3_pád': 'Krysodlakovi',
            'jméno_4_pád': 'Krysodlaka',
        },
    ),

    (
        Zvíře,
        {
            'jméno': 'Jeskynní dráček',
            'zdraví': 54,
            'útok': 9,
            'jméno_3_pád': 'Dráčkovi',
            'jméno_4_pád': 'Dráčka',
            'text_živý': 'Ze tmy vyskočil malý jeskynní dráček a zasáhl tě'
                         ' ohnivou koulí!',
            'text_mrtvý': 'Z mrtvoly jeskynního dráčka vytéká jasně oranžová'
                          ' tekutina.',
        },
    ),

    (
        Zvíře,
        {
            'jméno': 'Vlk',
            'zdraví': 28,
            'útok': 5,
            'jméno_3_pád': 'Vlkovi',
            'jméno_4_pád': 'Vlka',
            'text_živý': 'Z křoví na tebe vyskočil vychrtlý šedý vlk.',
        },
    ),

    (
        Netvor,
        {
            'jméno': 'Vlkodlak',
            'zdraví': 39,
            'útok': 9,
            'jméno_3_pád': 'Vlkodlakovi',
            'jméno_4_pád': 'Vlkodlaka',
        },
    ),
)


def náhodný_jeskynní_nepřítel():
    typ_nepřítele, parametry = random.choice(data_nepřátel[:6])
    return typ_nepřítele(**parametry)


def náhodný_lesní_nepřítel():
    typ_nepřítele, parametry = random.choice(data_nepřátel[6:])
    return typ_nepřítele(**parametry)
