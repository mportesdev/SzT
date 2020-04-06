import sys
sys.argv.append('--fast')

from hrac import Hráč
from utility import zjisti_možné_akce


def test_zakladni_pruchod_hrou():

    def jdi(cesta, cílová_pozice=None):
        for směr in cesta:
            místnost = hráč.místnost_pobytu()
            možnosti = zjisti_možné_akce(hráč)

            if směr not in možnosti:
                assert 'B' in možnosti
                # když vleze do místnosti s nepřítelem, dostane ránu
                místnost.dopad_na_hráče(hráč)
                assert hráč.žije(), (f'zabit na {hráč.x}, {hráč.y}'
                                     f' ({místnost.nepřítel})')

                # musí zabít nebo omráčit nepřítele, aby mohl jít dál
                while směr not in zjisti_možné_akce(hráč):
                    hráč.bojuj()
                    místnost.dopad_na_hráče(hráč)
                    assert hráč.žije(), (f'zabit na {hráč.x}, {hráč.y}'
                                         f' ({místnost.nepřítel})')

            akce = možnosti_pohybu.get(směr)
            akce()

        if cílová_pozice is not None:
            assert (hráč.x, hráč.y) == cílová_pozice

    def doplň_síly():
        if hráč.zdraví >= 100:
            return

        for věc in sorted((věc for věc in hráč.inventář
                          if hasattr(věc, 'léčivá_síla')),
                          key=lambda v: v.léčivá_síla, reverse=True):
            if věc.speciální:
                continue
            if věc.léčivá_síla <= 100 - hráč.zdraví:
                print(f'{věc}: {hráč.zdraví=}->', end='')
                hráč.spotřebuj(věc)
                print(hráč.zdraví)

    def seber_jednu_věc(*názvy):
        počet_věcí = len(hráč.inventář)
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
        assert len(hráč.inventář) == počet_věcí + 1
        sebraná_věc = hráč.inventář[-1]
        if názvy:
            assert sebraná_věc.název in názvy
        return sebraná_věc

    def seber_artefakt():
        počet_artefaktů = len(hráč.artefakty)
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
        assert len(hráč.artefakty) == počet_artefaktů + 1
        assert hráč.artefakty[-1].název in (
            'Křišťálová koule', 'Rubínový kříž', 'Tyrkysová tiára',
            'Ametystový kalich', 'Safírový trojzubec'
        )

    def seber_zlato():
        zlato = hráč.zlato
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
        assert hráč.zlato > zlato

    názvy_léčivek = ('Léčivé bylinky', 'Kouzelné bylinky', 'Léčivé houby',
                     'Kouzelné houby', 'Léčivé bobule', 'Kouzelné bobule',
                     'Plástev lesního medu', 'Hadí ocásek', 'Ještěrčí ocásek')

    názvy_zbraní = ('Cizokrajná šavle', 'Ostnatý palcát', 'Zkrvavená mačeta')

    hráč = Hráč()

    možnosti_pohybu = dict(S=hráč.jdi_na_sever,
                           J=hráč.jdi_na_jih,
                           Z=hráč.jdi_na_západ,
                           V=hráč.jdi_na_východ)

    # hráč stojí na začátku, je zdráv, má u sebe dvě věci, zatím si nedělá mapu
    assert hráč.místnost_pobytu() == hráč.svět.začátek
    assert (hráč.x, hráč.y) == (33, 27)
    assert hráč.zdraví == 100
    assert len(hráč.inventář) == 2
    nůž = hráč.inventář[0]
    assert hráč.nejlepší_zbraň() is nůž
    assert set(zjisti_možné_akce(hráč)) == set('SIK')

    # jde dál lesem
    jdi('SS')
    assert set(zjisti_možné_akce(hráč)) == set('SJIK')

    # dojde na první křižovatku a rozhodne se kreslit mapu
    jdi('S')
    assert set(zjisti_možné_akce(hráč)) == set('SJZIMK')

    # dojde na místo s bylinkami a sebere je
    jdi('SV')
    seber_jednu_věc('Léčivé bylinky')
    assert set(zjisti_možné_akce(hráč)) == set('ZIMK')

    # přes prvního nepřítele se probije nožem, dojde pro dýku a houby
    jdi('ZJZZSZZZZ', (27, 23))
    dýka = seber_jednu_věc('Rezavá dýka')
    assert hráč.nejlepší_zbraň() is dýka
    jdi('VJJVV', (30, 25))
    seber_jednu_věc('Léčivé houby')
    doplň_síly()

    # přejde přes dalšího nepřítele, dojde pro bobule a další lék
    jdi('ZZSSVSSVVSSS', (31, 18))
    seber_jednu_věc('Léčivé bobule')
    jdi('JZZSZZJJJ', (27, 21))
    seber_jednu_věc(*názvy_léčivek)
    doplň_síly()

    # přejde přes dalšího nepřítele, dojde pro další lék
    jdi('SZZZSZZSZ', (21, 18))
    seber_jednu_věc(*názvy_léčivek)

    # dojde k mastičkáři, prodá nůž a dýku za 11 + 27
    jdi('VJVVSSS', (24, 16))
    assert 'O' in zjisti_možné_akce(hráč)

    mastičkář = hráč.místnost_pobytu().obchodník
    zlato = hráč.zlato
    hráč.prodej(nůž, mastičkář)
    hráč.prodej(dýka, mastičkář)
    assert hráč.zlato == zlato + 11 + 27

    # koupí sekerku za 51 (v případě nedostatku peněz prodá ještě něco)
    sekerka = next(věc for věc in mastičkář.inventář if 'sekerka' in věc.název)
    while hráč.zlato < sekerka.cena and hráč.inventář:
        hráč.prodej(min(hráč.inventář, key=lambda v: v.cena), mastičkář)
    assert hráč.zlato >= sekerka.cena, 'chybí peníze na sekerku'
    hráč.kup(sekerka, mastičkář)
    assert hráč.nejlepší_zbraň() is sekerka
    doplň_síly()

    # sebere další lék
    jdi('JJJJJJZZZJ', (21, 23))
    seber_jednu_věc(*názvy_léčivek)
    doplň_síly()

    # přes nepřítele dojde pro lék
    jdi('SSSZZSZ', (18, 19))
    seber_jednu_věc(*názvy_léčivek)
    doplň_síly()

    # přes lesního trolla dojde pro meč
    jdi('VSSSZZJZZJ', (15, 18))
    meč_15x18 = seber_jednu_věc('Zrezivělý meč')
    assert hráč.nejlepší_zbraň() is meč_15x18
    doplň_síly()

    # sebere poslední lék v této části lesa
    jdi('SZSSVV', (16, 15))
    seber_jednu_věc(*názvy_léčivek)
    doplň_síly()

    # dojde k mastičkáři, prodá sekerku za 45
    jdi('ZZJJVVVSVVJJJJVVJJVVVSSSSSS', (24, 16))
    assert 'O' in zjisti_možné_akce(hráč)
    zlato = hráč.zlato
    hráč.prodej(sekerka, mastičkář)
    assert hráč.zlato == zlato + 45

    # koupí nejlepší léčiva, na která má peníze
    for léčivo in sorted((věc for věc in mastičkář.inventář
                          if hasattr(věc, 'léčivá_síla')),
                         key=lambda v: v.léčivá_síla, reverse=True):
        if léčivo.cena <= hráč.zlato:
            hráč.kup(léčivo, mastičkář)
            print(f'Koupil jsi {léčivo}')
    doplň_síly()

    # přes nepřítele dojde pro zlato
    jdi('SSVSSZ', (24, 12))
    doplň_síly()
    jdi('SS', (24, 10))
    seber_zlato()
    jdi('JJZZJJ', (22, 14))
    seber_zlato()

    # přes nepřítele dojde pro zbraň
    jdi('SSSSS', (22, 9))
    doplň_síly()
    jdi('ZZJJJZ', (19, 12))
    zbraň_19x12 = seber_jednu_věc(*názvy_zbraní)
    assert hráč.nejlepší_zbraň() is zbraň_19x12

    # dojde k mastičkáři, prodá meč za 62
    jdi('VSSSVVJJJVVVJJZJJ', (24, 16))
    assert 'O' in zjisti_možné_akce(hráč)
    zlato = hráč.zlato
    hráč.prodej(meč_15x18, mastičkář)
    assert hráč.zlato == zlato + 62

    # koupí nejlepší léčiva, na která má peníze
    for léčivo in sorted((věc for věc in mastičkář.inventář
                          if hasattr(věc, 'léčivá_síla')),
                         key=lambda v: v.léčivá_síla, reverse=True):
        if léčivo.cena <= hráč.zlato:
            hráč.kup(léčivo, mastičkář)
            print(f'Koupil jsi {léčivo}')
    doplň_síly()

    # vysbírá léčivky v jihovýchodním lese
    jdi('JJJJVVVSSVVJVVJJ', (31, 21))
    doplň_síly()
    jdi('ZZJJVVJVVSSSVVSVVSSVVVJ', (40, 19))
    seber_jednu_věc(*názvy_léčivek)
    doplň_síly()
    jdi('SZZZJJVJJJZZJJ', (36, 25))
    seber_jednu_věc(*názvy_léčivek)
    doplň_síly()
    jdi('SSVVVVJJJJZ', (39, 27))
    seber_jednu_věc(*názvy_léčivek)
    doplň_síly()

    # vrátí se do jeskyně
    jdi('VSSSSZZSSSZZZJZZJJJZZSZZSSVVSSZZSZZJJZZZSSSS', (24, 16))

    # přejde přes dalšího nepřítele pro zlato
    jdi('SSVSSZZZSSSZZJZZS', (18, 9))
    doplň_síly()
    jdi('SZZ', (16, 8))
    seber_zlato()

    # přejde přes dalšího nepřítele pro zlato
    jdi('ZJJJJZZ', (13, 12))
    doplň_síly()
    seber_zlato()

    # dojde pro nejbližší lék v druhém lese
    jdi('ZSSSZZZSZSZZS', (6, 6))
    seber_jednu_věc(*názvy_léčivek)

    # dojde ke zbrojíři, prodá zbraň a koupí meč za 114
    jdi('JVVJV', (9, 8))
    assert 'O' in zjisti_možné_akce(hráč)

    zbrojíř = hráč.místnost_pobytu().obchodník
    meč_9x8 = next(věc for věc in zbrojíř.inventář if 'meč' in věc.název)
    hráč.prodej(zbraň_19x12, zbrojíř)
    while hráč.zlato < meč_9x8.cena and hráč.inventář:
        hráč.prodej(min(hráč.inventář, key=lambda v: v.cena), zbrojíř)
    assert hráč.zlato >= meč_9x8.cena, 'chybí peníze na meč'
    hráč.kup(meč_9x8, zbrojíř)

    # přes trolla přejde pro lék a pro sekeru
    jdi('JVVVJVVVJVVSVVVSVVJJJVVVVSVVJ', (28, 12))
    doplň_síly()
    jdi('VVVVVSVVSV', (36, 10))
    seber_jednu_věc('Lahvička medicíny')
    doplň_síly()
    jdi('ZJZZJJVVJ', (35, 14))
    sekera = seber_jednu_věc('Těžká sekera')

    # vysbírá zlato v okolí
    jdi('SZZ', (33, 13))
    doplň_síly()
    jdi('SSSS', (33, 9))
    seber_zlato()
    jdi('JJJZZZJJ', (30, 14))
    seber_zlato()

    # dojde do severozápadního lesa
    jdi('SSZZSZZJZZZZSSSZZJZZZJZZSZZZSZZZSZ', (8, 8))

    # vysbírá tam léky
    jdi('SZZSSSZZ', (4, 4))
    doplň_síly()
    jdi('JJJZZSZSSVSSSZS', (1, 0))
    seber_jednu_věc(*názvy_léčivek)
    doplň_síly()
    jdi('JVJJJZJJVJJJZ', (1, 9))
    seber_jednu_věc(*názvy_léčivek)
    doplň_síly()
    jdi('ZJJVJJZ', (0, 13))
    seber_jednu_věc(*názvy_léčivek)
    doplň_síly()
    jdi('VSSZSSVVJVJJ', (3, 12))
    seber_jednu_věc(*názvy_léčivek)
    jdi('SSZSSSVVJ', (4, 8))
    seber_jednu_věc(*názvy_léčivek)
    doplň_síly()

    # vrátí se do jeskyně
    jdi('SSSSVVJJJVVJV', (9, 8))

    # dojde k odbočce do jihozápadní části jeskyně
    jdi('JVVVJJZZ', (10, 11))

    # přejde přes trolla
    jdi('JJZJ', (9, 14))
    doplň_síly()
    jdi('JJ', (9, 16))
    doplň_síly()

    # přejde přes další nepřátele, dojde pro zbraň, lék a první artefakt
    jdi('JJV', (10, 18))
    doplň_síly()
    jdi('JJVV', (12, 20))
    doplň_síly()
    jdi('JJZJ', (11, 23))
    zbraň_11x23 = seber_jednu_věc(*názvy_zbraní)

    jdi('SVVJVVSSSZ', (14, 20))
    seber_jednu_věc('Lahvička medicíny')
    doplň_síly()
    jdi('VJV', (16, 21))
    seber_artefakt()
    assert len(hráč.artefakty) == 1

    # probije se k druhému artefaktu
    jdi('ZJJZZSZSSZZSSZZZJJJZZZJZJ', (3, 23))
    doplň_síly()
    jdi('JV', (4, 24))
    seber_artefakt()
    assert len(hráč.artefakty) == 2

    # posbírá zlato
    jdi('ZSSVSVVJ', (6, 22))
    seber_zlato()

    jdi('SVSSSVVSSV', (10, 16))
    seber_zlato()

    jdi('ZSSSVSSZZZJ', (7, 12))
    doplň_síly()
    jdi('ZJ', (6, 13))
    seber_zlato()

    # vyrazí pro třetí artefakt
    jdi('SVSVVVVVSVVVJVVSVVVSVVSVVVVSS', (26, 6))
    doplň_síly()

    # probije se přes trolla
    jdi('VSVV', (29, 5))
    doplň_síly()
    jdi('JVVSVVJJV', (34, 7))
    seber_artefakt()
    assert len(hráč.artefakty) == 3

    # sebere lék
    jdi('ZSSSSZ', (32, 3))
    seber_jednu_věc('Lahvička medicíny')
    doplň_síly()

    # vysbírá zlato v okolí
    jdi('VJVVV', (36, 4))
    seber_zlato()
    jdi('ZZZJZZJZZSSVSSZ', (29, 2))
    doplň_síly()
    seber_zlato()
    jdi('VJJZJZZJZZZSSSV', (25, 3))
    seber_zlato()

    # přejde přes trolla
    jdi('ZJJJZZZ', (21, 6))
    doplň_síly()
    jdi('SS', (21, 4))
    doplň_síly()

    # sebere zbraň
    jdi('ZZZZJJV', (18, 6))
    zbraň_18x6 = seber_jednu_věc(*názvy_zbraní)

    # dojde ke zbrojíři koupit Smrtonoš
    jdi('ZSSVVVVJJVVVVVJJZZZZJZZJZZZJZZSZZZSZZZS', (9, 8))
    assert 'O' in zjisti_možné_akce(hráč)

    smrtonoš = next(věc for věc in zbrojíř.inventář if 'Smrtonoš' in věc.název)
    assert zbraň_11x23 in hráč.inventář
    hráč.prodej(zbraň_11x23, zbrojíř)
    assert zbraň_18x6 in hráč.inventář
    hráč.prodej(zbraň_18x6, zbrojíř)
    assert meč_9x8 in hráč.inventář
    hráč.prodej(meč_9x8, zbrojíř)
    assert sekera in hráč.inventář
    hráč.prodej(sekera, zbrojíř)
    assert hráč.zlato >= 256, 'chybí peníze na Smrtonoš'
    hráč.kup(smrtonoš, zbrojíř)

    # koupí léčiva tak, aby mu zbylo na elixír
    for léčivo in sorted((věc for věc in zbrojíř.inventář
                          if hasattr(věc, 'léčivá_síla')),
                         key=lambda v: v.léčivá_síla, reverse=True):
        if léčivo.cena <= hráč.zlato - 256:
            hráč.kup(léčivo, zbrojíř)
            print(f'Koupil jsi {léčivo}')
    doplň_síly()

    assert hráč.zlato >= 256, 'nezbývají peníze na elixír'

    # dojde k mastičkáři koupit elixír
    jdi('JVVVJVVVJVVSVVVSVVJJJVVVJJZJJ', (24, 16))
    assert 'O' in zjisti_možné_akce(hráč)
    elixír = next(věc for věc in mastičkář.inventář
                  if hasattr(věc, 'speciální') and věc.speciální)
    hráč.kup(elixír, mastičkář)

    # koupí zbylá léčiva
    for léčivo in sorted((věc for věc in mastičkář.inventář
                          if hasattr(věc, 'léčivá_síla')),
                         key=lambda v: v.léčivá_síla, reverse=True):
        if léčivo.cena <= hráč.zlato:
            hráč.kup(léčivo, mastičkář)
            print(f'Koupil jsi {léčivo}')
    doplň_síly()

    # přijde před dobrodruha
    jdi('SSVSSZZZSSSSVVVVSSZZZZZSSZZZZSZ', (16, 3))
    if elixír in hráč.inventář:
        print(f'{elixír}: {hráč.zdraví=} -> ', end='')
        hráč.spotřebuj(elixír)
        print(hráč.zdraví)

    # přejde přes dobrodruha
    jdi('ZZ', (14, 3))
    print(f'{hráč.zdraví=}')

    # sebere poslední lék
    jdi('SZZZZZSZ', (8, 1))
    seber_jednu_věc('Lahvička medicíny')
    doplň_síly()

    # vyrazí pro čtvrtý artefakt
    jdi('VJVVVVSSVVVJV', (17, 1))
    doplň_síly()
    jdi('VS', (18, 0))
    seber_artefakt()

    # vyrazí pro pátý artefakt
    jdi('JZZSZZZJJVJJJZZSZ', (11, 4))
    doplň_síly()
    jdi('ZJJ', (10, 6))
    seber_artefakt()

    # sebere zlato
    jdi('SSVVJVVSSSZZZSS', (11, 0))
    doplň_síly()
    jdi('Z', (10, 0))
    seber_zlato()

    # vyjde před jeskyni
    jdi('VJJVVVJVVVJVVVVJJVVJJZJJJJVVVJJZJJJ', (24, 17))

    # dojde na začátek a zvítězí
    jdi('JJJVVVSSVVJVVJJZZJJVVJVVJJJ', (33, 27))
    assert hráč.místnost_pobytu() == hráč.svět.začátek \
        and hráč.svět.poklad_posbírán()

    print(hráč.zkušenost)
    hráč.vypiš_věci()
