import sys
sys.argv.append('--fast')

from hrac import Hráč
from utility import zjisti_možné_akce


def test_zakladni_pruchod_hrou():

    def jdi(cesta):
        for směr in cesta:
            pohyb = dict(S=hráč.jdi_na_sever,
                         J=hráč.jdi_na_jih,
                         Z=hráč.jdi_na_západ,
                         V=hráč.jdi_na_východ).get(směr.upper())
            pohyb()

    def dostaň_ránu():
        zdraví = hráč.zdraví
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
        assert hráč.zdraví < zdraví
        možnosti = zjisti_možné_akce(hráč)
        assert 'B' in možnosti
        assert not any(klávesa in možnosti for klávesa in 'SJZV')

    def probojuj_se_na(směr):
        while směr.upper() not in zjisti_možné_akce(hráč):
            hráč.bojuj()
            hráč.místnost_pobytu().dopad_na_hráče(hráč)
            hráč.zdařilý_zásah = False
            assert hráč.žije(), 'K.I.A.'
        jdi(směr)

    def zab():
        while hráč.místnost_pobytu().nepřítel.žije():
            hráč.bojuj()
            hráč.místnost_pobytu().dopad_na_hráče(hráč)
            hráč.zdařilý_zásah = False
            assert hráč.žije(), 'K.I.A.'

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

    def seber_zlato():
        zlato = hráč.zlato
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
        assert hráč.zlato > zlato

    názvy_léčivek = ('Léčivé houby', 'Léčivé bobule', 'Léčivé bylinky',
                     'Kouzelné houby', 'Kouzelné bobule')

    hráč = Hráč()

    # hráč stojí na začátku, je zdráv, má u sebe dvě věci, zatím si nedělá mapu
    assert (hráč.x, hráč.y) == (hráč.svět.začátek.x, hráč.svět.začátek.y)
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

    # dojde na místo s nepřítelem, probije se dál na západ
    jdi('ZJZZSZ')
    dostaň_ránu()
    probojuj_se_na('Z')

    # dojde na místo s dýkou a sebere ji
    jdi('ZZ')
    dýka = seber_jednu_věc('Rezavá dýka')
    assert hráč.nejlepší_zbraň() is dýka
    doplň_síly()

    # dojde na místo s houbami a sebere je
    jdi('VJJVV')
    seber_jednu_věc('Léčivé houby')

    # dojde na místo s dalším nepřítelem, probije se dál na sever
    jdi('ZZSSVSSVVS')
    dostaň_ránu()
    probojuj_se_na('S')

    # dojde na místo s bobulemi a sebere je
    hráč.jdi_na_sever()
    seber_jednu_věc('Léčivé bobule')
    doplň_síly()

    # dojde na místo s dalším lékem a sebere ho
    jdi('JZZSZZJJJ')
    seber_jednu_věc(*názvy_léčivek)

    # dojde na místo s dalším nepřítelem, probije se dál na západ
    jdi('SZZ')
    dostaň_ránu()
    probojuj_se_na('Z')
    doplň_síly()

    # stojí na severo-jižní cestě poblíž vchodu do jeskyně
    assert (hráč.x, hráč.y) == (24, 20)

    # sebere další lék
    jdi('SZZSZ')
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

    # dojde na místo s dalším nepřítelem, probije se dál na sever
    jdi('SS')
    dostaň_ránu()
    probojuj_se_na('S')
    doplň_síly()

    # sebere další lék
    jdi('ZZSZ')
    seber_jednu_věc(*názvy_léčivek)

    # dojde na místo s lesním trollem, probije se dál na sever
    jdi('VSS')
    dostaň_ránu()
    probojuj_se_na('S')
    doplň_síly()

    # dojde na místo s mečem a sebere ho
    jdi('ZZJZZJ')
    meč = seber_jednu_věc('Zrezivělý meč')
    assert hráč.nejlepší_zbraň() is meč

    # dojde na místo s dalším nepřítelem, probije se dál na východ
    jdi('SZSS')
    dostaň_ránu()
    probojuj_se_na('V')

    # sebere poslední lék v této části lesa
    hráč.jdi_na_východ()
    seber_jednu_věc(*názvy_léčivek)
    doplň_síly()

    # dojde na místo s nepřítelem a pokud ještě žije, zkusí přes něj přejít
    jdi('ZZ')
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    probojuj_se_na('J')

    # totéž udělá s dalším nepřítelem
    jdi('JVVVSVVJJJJVVJ')
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    probojuj_se_na('J')

    # dojde k mastičkáři, prodá sekerku za 45
    jdi('VVVSSSSSS')
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

    # dojde k prvnímu jeskynnímu nepříteli, probije se dál na západ
    jdi('SSVSS')
    dostaň_ránu()
    probojuj_se_na('Z')

    # vysbírá zlato v blízkém okolí
    jdi('SS')
    seber_zlato()
    jdi('JJZZJJ')
    seber_zlato()

    # dojde ke druhému jeskynnímu nepříteli, probije se dál na sever
    jdi('SSSS')
    dostaň_ránu()
    probojuj_se_na('S')
    doplň_síly()

    # dojde na místo se zbraní (palcát, řemdih nebo mačeta) a sebere ji
    jdi('ZZJJJZ')
    zbraň_19x12 = seber_jednu_věc('Ostnatý palcát', 'Damascénská mačeta',
                                  'Řemdih')
    assert hráč.nejlepší_zbraň() is zbraň_19x12

    # dojde na místo s nepřítelem a pokud ještě žije, zabije ho
    jdi('VSSSVVJ')
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    zab()

    # totéž udělá s dalším nepřítelem
    jdi('JJVVV')
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    zab()

    # dojde k mastičkáři, prodá meč za 62
    jdi('JJZJJ')
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

    # dojde k dalšímu nepříteli, probije se dál na sever
    jdi('SSVSSZZZSSSZZJZZ')
    dostaň_ránu()
    probojuj_se_na('S')
    doplň_síly()

    # sebere zlato
    jdi('SZZ')
    seber_zlato()

    jdi('ZJJ')

    # stojí na křižovatce v pomyslném středu jeskyně
    assert (hráč.x, hráč.y) == (15, 10)

    # dojde k dalšímu nepříteli, probije se dál na západ
    jdi('JJZ')
    dostaň_ránu()
    probojuj_se_na('Z')

    # sebere zlato
    seber_zlato()
    doplň_síly()

    # dojde pro nejbližší lék v druhém lese
    jdi('ZSSSZZZSZSZZS')
    seber_jednu_věc(*názvy_léčivek)

    # dojde ke zbrojíři, prodá zbraň a koupí těžkou sekeru za 121
    jdi('JVVJV')
    assert 'O' in zjisti_možné_akce(hráč)

    zbrojíř = hráč.místnost_pobytu().obchodník
    sekera = next(věc for věc in zbrojíř.inventář if 'sekera' in věc.název)
    hráč.prodej(zbraň_19x12, zbrojíř)
    while hráč.zlato < sekera.cena and hráč.inventář:
        hráč.prodej(hráč.inventář[-1], zbrojíř)
    assert hráč.zlato >= 121, f'nejsou peníze na sekeru! ({hráč.zlato})'
    hráč.kup(sekera, zbrojíř)
    hráč.vypiš_věci()

    # dojde k trollovi, probije se dál na východ
    jdi('JVVVJVVVJVVSVVVSVVJJJVVVVSVVJV')
    dostaň_ránu()
    probojuj_se_na('V')

    # dojde pro lék
    jdi('VVVSVVSV')
    seber_jednu_věc('Lahvička medicíny')
    doplň_síly()

    # dojde k dalšímu nepříteli, probije se dál na východ
    jdi('ZJZZJJV')
    dostaň_ránu()
    probojuj_se_na('V')

    # dojde pro zbraň
    hráč.jdi_na_jih()
    zbraň_35x14 = seber_jednu_věc()

    # dojde na místo s nepřítelem a pokud ještě žije, zkusí přes něj přejít
    jdi('SZ')
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    probojuj_se_na('Z')

    # vysbírá zlato v okolí
    jdi('SSSS')
    seber_zlato()
    jdi('JJJZZZJJ')
    seber_zlato()

    # dojde k prvnímu nepříteli v druhém lese, zabije ho
    jdi('SSZZSZZJZZZZSSSZZJZZZJZZSZZZSZZZSZSZZSSSZ')
    dostaň_ránu()
    zab()

    # dojde k dalšímu nepříteli, zabije ho
    jdi('ZJJJZZSZSSVS')
    dostaň_ránu()
    zab()

    # sebere lék úplně na severu
    jdi('SSZS')
    seber_jednu_věc(*názvy_léčivek)

    # dojde k dalšímu nepříteli, zabije ho
    jdi('JVJJJZJJVJJ')
    dostaň_ránu()
    zab()

    # sebere lék
    jdi('JZ')
    seber_jednu_věc(*názvy_léčivek)

    # dojde k dalšímu nepříteli, zabije ho
    jdi('ZJJVJ')
    dostaň_ránu()
    zab()

    # vysbírá ostatní léky
    jdi('JZ')
    seber_jednu_věc(*názvy_léčivek)
    jdi('VSSZSSVVJVJJ')
    seber_jednu_věc(*názvy_léčivek)
    jdi('SSZSSSVVJ')
    seber_jednu_věc(*názvy_léčivek)
    doplň_síly()
