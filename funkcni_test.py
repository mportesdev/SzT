import sys
sys.argv.append('--fast')

from hrac import Hráč
from utility import zjisti_možné_akce


def test_zakladni_pruchod_hrou():

    def jdi(cesta):
        for směr in cesta:
            možnosti = zjisti_možné_akce(hráč)

            if směr not in možnosti:
                assert 'B' in možnosti
                # když vleze do místnosti s nepřítelem, dostane ránu
                hráč.místnost_pobytu().dopad_na_hráče(hráč)
                assert hráč.žije(), 'zabit v boji'

                # musí zabít nebo omráčit nepřítele, aby mohl jít dál
                while směr not in zjisti_možné_akce(hráč):
                    hráč.bojuj()
                    hráč.místnost_pobytu().dopad_na_hráče(hráč)
                    assert hráč.žije(), 'zabit v boji'

            akce = dict(S=hráč.jdi_na_sever,
                        J=hráč.jdi_na_jih,
                        Z=hráč.jdi_na_západ,
                        V=hráč.jdi_na_východ).get(směr)
            akce()

    def doplň_síly():
        for věc in hráč.inventář.copy():
            try:
                if věc.léčivá_síla <= 100 - hráč.zdraví:
                    print(f'{věc}: {hráč.zdraví=}->', end='')
                    hráč.spotřebuj(věc)
                    print(hráč.zdraví)
            except AttributeError:
                continue

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

    názvy_léčivek = ('Léčivé houby', 'Léčivé bobule', 'Léčivé bylinky',
                     'Kouzelné houby', 'Kouzelné bobule')

    názvy_zbraní = ('Srp a kladivo', 'Ostnatý palcát', 'Zkrvavená mačeta')

    hráč = Hráč()

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
    jdi('ZJZZSZZZZ')
    dýka = seber_jednu_věc('Rezavá dýka')
    assert hráč.nejlepší_zbraň() is dýka
    doplň_síly()
    jdi('VJJVV')
    assert (hráč.x, hráč.y) == (30, 25)
    seber_jednu_věc('Léčivé houby')

    # přejde přes dalšího nepřítele, dojde pro bobule a další lék
    jdi('ZZSSVSSVVSSS')
    seber_jednu_věc('Léčivé bobule')
    doplň_síly()
    jdi('JZZSZZJJJ')
    assert (hráč.x, hráč.y) == (27, 21)
    seber_jednu_věc(*názvy_léčivek)
    doplň_síly()

    # přejde přes dalšího nepřítele, dojde pro další lék
    jdi('SZZZSZZSZ')
    assert (hráč.x, hráč.y) == (21, 18)
    seber_jednu_věc(*názvy_léčivek)

    # dojde k mastičkáři, prodá nůž a dýku za 11 + 27
    jdi('VJVVSSS')
    assert (hráč.x, hráč.y) == (24, 16)
    assert 'O' in zjisti_možné_akce(hráč)

    mastičkář = hráč.místnost_pobytu().obchodník
    zlato = hráč.zlato
    hráč.prodej(nůž, mastičkář)
    hráč.prodej(dýka, mastičkář)
    assert hráč.zlato == zlato + 11 + 27

    # koupí sekerku za 51 (v případě nedostatku peněz prodá ještě něco)
    sekerka = next(věc for věc in mastičkář.inventář if 'sekerka' in věc.název)
    while hráč.zlato < sekerka.cena:
        hráč.prodej(min((věc for věc in hráč.inventář
                         if věc.cena >= sekerka.cena - hráč.zlato),
                        key=lambda v: v.cena),
                    mastičkář)
    hráč.kup(sekerka, mastičkář)
    assert hráč.nejlepší_zbraň() is sekerka
    hráč.vypiš_věci()

    # sebere další lék
    jdi('JJJJJJZZZJ')
    assert (hráč.x, hráč.y) == (21, 23)
    seber_jednu_věc(*názvy_léčivek)

    # přes nepřítele dojde pro lék
    jdi('SSSZZSZ')
    assert (hráč.x, hráč.y) == (18, 19)
    seber_jednu_věc(*názvy_léčivek)
    doplň_síly()

    # přes lesního trolla dojde pro meč
    jdi('VSSSZZJZZJ')
    assert (hráč.x, hráč.y) == (15, 18)
    meč = seber_jednu_věc('Zrezivělý meč')
    assert hráč.nejlepší_zbraň() is meč
    doplň_síly()

    # sebere poslední lék v této části lesa
    jdi('SZSSVV')
    assert (hráč.x, hráč.y) == (16, 15)
    seber_jednu_věc(*názvy_léčivek)
    doplň_síly()

    # dojde k mastičkáři, prodá sekerku za 45
    jdi('ZZJJVVVSVVJJJJVVJJVVVSSSSSS')
    assert (hráč.x, hráč.y) == (24, 16)
    assert 'O' in zjisti_možné_akce(hráč)
    zlato = hráč.zlato
    hráč.prodej(sekerka, mastičkář)
    assert hráč.zlato == zlato + 45

    # koupí nejlepší léčiva, na která má peníze
    for léčivo in sorted((věc for věc in mastičkář.inventář
                          if hasattr(věc, 'léčivá_síla')),
                         key=lambda v: v.léčivá_síla,
                         reverse=True):
        if léčivo.cena <= hráč.zlato:
            hráč.kup(léčivo, mastičkář)
            print(f'Koupil jsi {léčivo}')
    hráč.vypiš_věci()
    doplň_síly()

    # přes nepřítele dojde pro zlato
    jdi('SSVSSZSS')
    assert (hráč.x, hráč.y) == (24, 10)
    seber_zlato()
    jdi('JJZZJJ')
    assert (hráč.x, hráč.y) == (22, 14)
    seber_zlato()

    # přes nepřítele dojde pro zbraň
    jdi('SSSSSZZJJJZ')
    assert (hráč.x, hráč.y) == (19, 12)
    doplň_síly()
    zbraň_19x12 = seber_jednu_věc(*názvy_zbraní)
    assert hráč.nejlepší_zbraň() is zbraň_19x12

    # dojde k mastičkáři, prodá meč za 62
    jdi('VSSSVVJJJVVVJJZJJ')
    assert (hráč.x, hráč.y) == (24, 16)
    assert 'O' in zjisti_možné_akce(hráč)
    zlato = hráč.zlato
    hráč.prodej(meč, mastičkář)
    assert hráč.zlato == zlato + 62
    hráč.vypiš_věci()

    # koupí nejlepší léčiva, na která má peníze
    for léčivo in sorted((věc for věc in mastičkář.inventář
                          if hasattr(věc, 'léčivá_síla')),
                         key=lambda v: v.léčivá_síla,
                         reverse=True):
        if léčivo.cena <= hráč.zlato:
            hráč.kup(léčivo, mastičkář)
            print(f'Koupil jsi {léčivo}')
    hráč.vypiš_věci()
    doplň_síly()

    # přejde přes dalšího nepřítele pro zlato
    jdi('SSVSSZZZSSSZZJZZSSZZ')
    assert (hráč.x, hráč.y) == (16, 8)
    seber_zlato()
    doplň_síly()

    # přejde přes dalšího nepřítele pro zlato
    jdi('ZJJJJZZ')
    assert (hráč.x, hráč.y) == (13, 12)
    seber_zlato()
    doplň_síly()

    # dojde pro nejbližší lék v druhém lese
    jdi('ZSSSZZZSZSZZS')
    assert (hráč.x, hráč.y) == (6, 6)
    seber_jednu_věc(*názvy_léčivek)

    # dojde ke zbrojíři, prodá zbraň a koupí meč za 114
    jdi('JVVJV')
    assert (hráč.x, hráč.y) == (9, 8)
    assert 'O' in zjisti_možné_akce(hráč)

    zbrojíř = hráč.místnost_pobytu().obchodník
    meč = next(věc for věc in zbrojíř.inventář if 'meč' in věc.název)
    hráč.prodej(zbraň_19x12, zbrojíř)
    while hráč.zlato < meč.cena and hráč.inventář:
        hráč.prodej(hráč.inventář[-1], zbrojíř)
    assert hráč.zlato >= 114, 'chybí peníze na meč'
    hráč.kup(meč, zbrojíř)
    hráč.vypiš_věci()

    # přes trolla přejde pro lék a pro sekeru
    jdi('JVVVJVVVJVVSVVVSVVJJJVVVVSVVJ')
    assert (hráč.x, hráč.y) == (28, 12)
    doplň_síly()
    jdi('VVVVVSVVSV')
    assert (hráč.x, hráč.y) == (36, 10)
    seber_jednu_věc('Lahvička medicíny')
    doplň_síly()
    jdi('ZJZZJJVVJ')
    assert (hráč.x, hráč.y) == (35, 14)
    sekera = seber_jednu_věc('Těžká sekera')

    # vysbírá zlato v okolí
    jdi('SZZSSSS')
    assert (hráč.x, hráč.y) == (33, 9)
    seber_zlato()
    jdi('JJJZZZJJ')
    assert (hráč.x, hráč.y) == (30, 14)
    seber_zlato()

    # dojde do severozápadního lesa
    jdi('SSZZSZZJZZZZSSSZZJZZZJZZSZZZSZZZSZ')
    assert (hráč.x, hráč.y) == (8, 8)

    # vysbírá tam léky
    jdi('SZZSSSZZJJJZZSZSSVSSSZS')
    assert (hráč.x, hráč.y) == (1, 0)
    seber_jednu_věc(*názvy_léčivek)
    jdi('JVJJJZJJVJJJZ')
    assert (hráč.x, hráč.y) == (1, 9)
    seber_jednu_věc(*názvy_léčivek)
    jdi('ZJJVJJZ')
    assert (hráč.x, hráč.y) == (0, 13)
    seber_jednu_věc(*názvy_léčivek)
    jdi('VSSZSSVVJVJJ')
    assert (hráč.x, hráč.y) == (3, 12)
    seber_jednu_věc(*názvy_léčivek)
    jdi('SSZSSSVVJ')
    assert (hráč.x, hráč.y) == (4, 8)
    seber_jednu_věc(*názvy_léčivek)
    doplň_síly()

    # vrátí se do jeskyně
    jdi('SSSSVVJJJVVJV')
    assert (hráč.x, hráč.y) == (9, 8)
    # dojde k odbočce do jihozápadní části jeskyně
    jdi('JVVVJJZZ')
    assert (hráč.x, hráč.y) == (10, 11)

    # přejde přes trolla
    jdi('JJZJJJ')
    assert (hráč.x, hráč.y) == (9, 16)
    doplň_síly()

    # přejde přes další nepřátele, dojde pro zbraň, lék a první artefakt
    jdi('JJVJJVVJJZJ')
    assert (hráč.x, hráč.y) == (11, 23)
    zbraň_11x23 = seber_jednu_věc(*názvy_zbraní)

    jdi('SVVJVVSSSZ')
    assert (hráč.x, hráč.y) == (14, 20)
    seber_jednu_věc('Lahvička medicíny')
    doplň_síly()
    jdi('VJV')
    assert (hráč.x, hráč.y) == (16, 21)
    seber_artefakt()
    assert len(hráč.artefakty) == 1

    # probije se k druhému artefaktu
    jdi('ZJJZZSZSSZZSSZZZJJJZZZJZJJV')
    assert (hráč.x, hráč.y) == (4, 24)
    seber_artefakt()
    assert len(hráč.artefakty) == 2
    hráč.vypiš_věci()

    # posbírá zlato
    jdi('ZSSVSVVJ')
    assert (hráč.x, hráč.y) == (6, 22)
    seber_zlato()

    jdi('SVSSSVVSSV')
    assert (hráč.x, hráč.y) == (10, 16)
    seber_zlato()

    jdi('ZSSSVSSZZZJZJ')
    assert (hráč.x, hráč.y) == (6, 13)
    seber_zlato()

    # vyrazí pro třetí artefakt
    jdi('SVSVVVVVSVVVJVVSVVVSVVSVVVVSSVSVV')
    assert (hráč.x, hráč.y) == (29, 5)
    doplň_síly()
    jdi('JVVSVVJJV')
    assert (hráč.x, hráč.y) == (34, 7)
    seber_artefakt()
    assert len(hráč.artefakty) == 3
    hráč.vypiš_věci()

    # sebere lék
    jdi('ZSSSSZ')
    assert (hráč.x, hráč.y) == (32, 3)
    seber_jednu_věc('Lahvička medicíny')
    doplň_síly()

    # vysbírá zlato v okolí
    jdi('VJVVV')
    assert (hráč.x, hráč.y) == (36, 4)
    seber_zlato()
    jdi('ZZZJZZJZZSSVSSZ')
    assert (hráč.x, hráč.y) == (29, 2)
    seber_zlato()
    jdi('VJJZJZZJZZZSSSV')
    assert (hráč.x, hráč.y) == (25, 3)
    seber_zlato()

    # přejde přes trolla
    jdi('ZJJJZZZSS')
    assert (hráč.x, hráč.y) == (21, 4)
    doplň_síly()

    # sebere zbraň
    jdi('ZZZZJJV')
    assert (hráč.x, hráč.y) == (18, 6)

    # přejde přes dobrodruha
    jdi('ZSSSZZZ')
    assert (hráč.x, hráč.y) == (14, 3)

    # sebere poslední lék
    jdi('SZZZZZSZ')
    assert (hráč.x, hráč.y) == (8, 1)
    seber_jednu_věc('Lahvička medicíny')
    doplň_síly()

    # vyrazí pro čtvrtý artefakt
    jdi('VJVVVVSSVVVJVVS')
    assert (hráč.x, hráč.y) == (18, 0)
    seber_artefakt()

    # vyrazí pro pátý artefakt
    jdi('JZZSZZZJJVJJJZZSZZJJ')
    assert (hráč.x, hráč.y) == (10, 6)
    seber_artefakt()

    # sebere zlato
    jdi('SSVVJVVSSSZZZSSZ')
    assert (hráč.x, hráč.y) == (10, 0)
    seber_zlato()

    # vyjde před jeskyni
    jdi('VJJVVVJVVVJVVVVJJVVJJZJJJJVVVJJZJJJ')
    assert (hráč.x, hráč.y) == (24, 17)

    # dojde na začátek a zvítězí
    jdi('JJJVVVSSVVJVVJJZZJJVVJVVJJJ')
    assert (hráč.x, hráč.y) == (33, 27)
    assert hráč.místnost_pobytu() == hráč.svět.začátek \
        and hráč.svět.poklad_posbírán()

    print(hráč.zkušenost)
    hráč.vypiš_věci()
