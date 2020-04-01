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

    hráč = Hráč()

    # hráč stojí na začátku, je zdráv, má u sebe dvě věci, zatím si nedělá mapu
    assert hráč.místnost_pobytu() == hráč.svět.začátek
    assert hráč.zdraví == 100
    assert len(hráč.inventář) == 2
    nůž = hráč.inventář[0]
    assert hráč.nejlepší_zbraň() is nůž
    assert set(zjisti_možné_akce(hráč)) == set('SIK')

    # jde dál lesem
    jdi('SS')
    assert set(zjisti_možné_akce(hráč)) == set('SJIK')

    # dojde na první křižovatku a rozhodne se kreslit mapu
    hráč.jdi_na_sever()
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
    seber_jednu_věc('Léčivé houby')

    # přejde přes dalšího nepřítele, dojde pro bobule a další lék
    jdi('ZZSSVSSVVSSS')
    seber_jednu_věc('Léčivé bobule')
    doplň_síly()
    jdi('JZZSZZJJJ')
    seber_jednu_věc(*názvy_léčivek)
    doplň_síly()

    # přejde přes dalšího nepřítele, dojde pro další lék
    jdi('SZZZSZZSZ')
    seber_jednu_věc(*názvy_léčivek)

    # dojde k mastičkáři, prodá nůž a dýku za 11 + 27
    jdi('VJVVSSS')
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
    seber_jednu_věc(*názvy_léčivek)

    # přes nepřítele dojde pro lék
    jdi('SSSZZSZ')
    seber_jednu_věc(*názvy_léčivek)
    doplň_síly()

    # přes lesního trolla dojde pro meč
    jdi('VSSSZZJZZJ')
    meč = seber_jednu_věc('Zrezivělý meč')
    assert hráč.nejlepší_zbraň() is meč
    doplň_síly()

    # sebere poslední lék v této části lesa
    jdi('SZSSVV')
    seber_jednu_věc(*názvy_léčivek)
    doplň_síly()

    # dojde k mastičkáři, prodá sekerku za 45
    jdi('ZZJJVVVSVVJJJJVVJJVVVSSSSSS')
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
    seber_zlato()
    jdi('JJZZJJ')
    seber_zlato()

    # přes nepřítele dojde pro zbraň (palcát, řemdih nebo mačeta)
    jdi('SSSSS')
    doplň_síly()
    jdi('ZZJJJZ')
    zbraň_19x12 = seber_jednu_věc('Srp a kladivo', 'Ostnatý palcát',
                                  'Ohořelý trojzubec', 'Řemdih')
    assert hráč.nejlepší_zbraň() is zbraň_19x12

    # dojde k mastičkáři, prodá meč za 62
    jdi('VSSSVVJJJVVVJJZJJ')
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

    # přejde přes další nepřátele
    jdi('SSVSSZZZSSSZZJZZ')

    # stojí na křižovatce v pomyslném středu jeskyně
    assert (hráč.x, hráč.y) == (18, 10)

    # dojde pro zlato
    jdi('S')
    doplň_síly()
    jdi('SZZ')
    seber_zlato()

    # přes nepřítele dojde pro zlato
    jdi('ZJJJJZZ')
    seber_zlato()
    doplň_síly()

    # dojde pro nejbližší lék v druhém lese
    jdi('ZSSSZZZSZSZZS')
    seber_jednu_věc(*názvy_léčivek)

    # dojde ke zbrojíři, prodá zbraň a koupí meč za 114
    jdi('JVVJV')
    assert 'O' in zjisti_možné_akce(hráč)

    zbrojíř = hráč.místnost_pobytu().obchodník
    meč = next(věc for věc in zbrojíř.inventář if 'meč' in věc.název)
    hráč.prodej(zbraň_19x12, zbrojíř)
    while hráč.zlato < meč.cena and hráč.inventář:
        hráč.prodej(hráč.inventář[-1], zbrojíř)
    assert hráč.zlato >= 114, 'chybí peníze na meč'
    hráč.kup(meč, zbrojíř)
    hráč.vypiš_věci()

    # přes trolla přejde pro lék a pro zbraň
    jdi('JVVVJVVVJVVSVVVSVVJJJVVVVSVVJVVVVVSVVSV')
    seber_jednu_věc('Lahvička medicíny')
    doplň_síly()
    jdi('ZJZZJJVVJ')
    sekera = seber_jednu_věc('Těžká sekera')
    assert (hráč.x, hráč.y) == (35, 14)

    # vysbírá zlato v okolí
    jdi('SZZSSSS')
    seber_zlato()
    jdi('JJJZZZJJ')
    seber_zlato()

    # dojde do severozápadního lesa
    jdi('SSZZSZZJZZZZSSSZZJZZZJZZSZZZSZZZSZ')
    assert (hráč.x, hráč.y) == (8, 8)

    # vysbírá tam léky
    jdi('SZZSSSZZJJJZZSZSSVSSSZS')
    seber_jednu_věc(*názvy_léčivek)
    jdi('JVJJJZJJVJJJZ')
    seber_jednu_věc(*názvy_léčivek)
    jdi('ZJJVJJZ')
    seber_jednu_věc(*názvy_léčivek)
    jdi('VSSZSSVVJVJJ')
    seber_jednu_věc(*názvy_léčivek)
    jdi('SSZSSSVVJ')
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
    doplň_síly()

    # přejde přes další nepřátele, dojde pro lék a první artefakt
    jdi('JJVJJVVJJVJVVSSSZ')
    seber_jednu_věc('Lahvička medicíny')
    doplň_síly()
    jdi('VJV')
    seber_artefakt()

    # probije se k druhému artefaktu
    jdi('ZJJZZSZSSZZSSZZZJJJZZZJZJJV')
    seber_artefakt()
    hráč.vypiš_věci()

    # vyrazí pro třetí artefakt
    jdi('ZSSVSVVVSSSVVSSSSSVSSVVSVVV')
    assert (hráč.x, hráč.y) == (15, 10)
    jdi('JVVSVVVSVVSVVVVSSVSVV')
    doplň_síly()
    jdi('JVVSVVJJV')
    seber_artefakt()
    hráč.vypiš_věci()

    # sebere lék
    jdi('ZSSSSZ')
    seber_jednu_věc('Lahvička medicíny')
    doplň_síly()

    # vysbírá zlato v okolí
    jdi('VJVVV')
    seber_zlato()
    jdi('ZZZJZZJZZSSVSSZ')
    seber_zlato()
    jdi('VJJZJZZJZZZSSSV')
    seber_zlato()

    # přejde přes trolla
    jdi('ZJJJZZZSS')
    doplň_síly()
    # přejde přes dobrodruha
    jdi('ZZZZSZZZ')

    # sebere poslední lék
    jdi('SZZZZZSZ')
    seber_jednu_věc('Lahvička medicíny')
    doplň_síly()

    # vyrazí pro čtvrtý artefakt
    jdi('VJVVVVSSVVVJVVS')
    seber_artefakt()

    # vyrazí pro pátý artefakt
    jdi('JZZSZZZJJVJJJZZSZZJJ')
    seber_artefakt()

    # sebere zlato
    jdi('SSVVJVVSSSZZZSSZ')
    seber_zlato()

    # vyjde před jeskyni
    jdi('VJJVVVJVVVJVVVVJJVVJJZJJJJVVVJJZJJJ')
    assert (hráč.x, hráč.y) == (24, 17)

    # dojde na začátek a zvítězí
    jdi('JJJVVVSSVVJVVJJZZJJVVJVVJJJ')
    assert hráč.místnost_pobytu() == hráč.svět.začátek and hráč.svět.poklad_posbírán()

    print(hráč.zkušenost)
    hráč.vypiš_věci()
