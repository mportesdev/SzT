import sys
sys.argv.append('--fast')

from hrac import Hráč
from utility import zjisti_možné_akce


def jdi(hráč, cesta):
    for směr in cesta:
        pohyb = dict(S=hráč.jdi_na_sever,
                     J=hráč.jdi_na_jih,
                     Z=hráč.jdi_na_západ,
                     V=hráč.jdi_na_východ).get(směr.upper())
        pohyb()


def test_zakladni_pruchod_hrou():
    hráč = Hráč()

    # hráč stojí na začátku, je zdráv, má u sebe dvě věci, zatím si nedělá mapu
    # TODO: aktivace mapy az na prvni krizovatce
    assert (hráč.x, hráč.y) == (hráč.svět.začátek.x, hráč.svět.začátek.y)
    assert hráč.zdraví == 100
    assert len(hráč.inventář) == 2
    nůž = hráč.inventář[0]
    assert hráč.nejlepší_zbraň() is nůž
    # assert set(zjisti_možné_akce(hráč).keys()) == set('SIK')

    # jde dál lesem
    jdi(hráč, 'SS')
    # assert set(zjisti_možné_akce(hráč).keys()) == set('SJIK')

    # dojde na první křižovatku a rozhodne se kreslit mapu
    hráč.jdi_na_sever()
    assert set(zjisti_možné_akce(hráč).keys()) == set('SJZIMK')

    # dojde na místo s bylinkami a sebere je
    jdi(hráč, 'SV')
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert len(hráč.inventář) == 3
    assert hráč.inventář[-1].název == 'Léčivé bylinky'
    assert set(zjisti_možné_akce(hráč).keys()) == set('ZIMK')

    # dojde na místo s nepřítelem a utrpí zranění
    jdi(hráč, 'ZJZZSZ')
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.zdraví < 100
    možnosti = zjisti_možné_akce(hráč)
    assert 'B' in možnosti
    assert not any(klávesa in možnosti for klávesa in 'SJZV')

    # pokusí se probít dál na západ
    while 'Z' not in zjisti_možné_akce(hráč):
        hráč.bojuj()
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
        assert hráč.žije(), 'K.I.A.'
    hráč.jdi_na_západ()

    # dojde na místo s dýkou a sebere ji
    jdi(hráč, 'ZZ')
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert len(hráč.inventář) == 4
    dýka = hráč.inventář[-1]
    assert hráč.nejlepší_zbraň() is dýka
    assert dýka.název == 'Rezavá dýka'

    # zkusí se trochu vyléčit
    for věc in hráč.inventář.copy():
        try:
            if věc.léčivá_síla <= 100 - hráč.zdraví:
                print(f'{věc}: {hráč.zdraví=}->', end='')
                hráč.spotřebuj(věc)
                print(hráč.zdraví)
        except AttributeError:
            continue

    # dojde na místo s houbami a sebere je
    jdi(hráč, 'VJJVV')
    počet_věcí = len(hráč.inventář)
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert len(hráč.inventář) == počet_věcí + 1
    assert hráč.inventář[-1].název == 'Léčivé houby'

    # dojde na místo s dalším nepřítelem a utrpí zranění
    jdi(hráč, 'ZZSSVSSVVS')
    zdraví = hráč.zdraví
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.zdraví < zdraví
    možnosti = zjisti_možné_akce(hráč)
    assert 'B' in možnosti
    assert not any(klávesa in možnosti for klávesa in 'SJZV')

    # pokusí se probít dál na sever
    while 'S' not in zjisti_možné_akce(hráč):
        hráč.bojuj()
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
        assert hráč.žije(), 'K.I.A.'
    hráč.jdi_na_sever()

    # dojde na místo s bobulemi a sebere je
    hráč.jdi_na_sever()
    počet_věcí = len(hráč.inventář)
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert len(hráč.inventář) == počet_věcí + 1
    assert hráč.inventář[-1].název == 'Léčivé bobule'

    # zkusí se trochu vyléčit
    for věc in hráč.inventář.copy():
        try:
            if věc.léčivá_síla <= 100 - hráč.zdraví:
                print(f'{věc}: {hráč.zdraví=}->', end='')
                hráč.spotřebuj(věc)
                print(hráč.zdraví)
        except AttributeError:
            continue

    # dojde na místo s další léčivkou a sebere ji
    jdi(hráč, 'JZZSZZJJJ')
    počet_věcí = len(hráč.inventář)
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert len(hráč.inventář) == počet_věcí + 1
    assert hráč.inventář[-1].název.endswith(('houby', 'bobule', 'bylinky'))

    # dojde na místo s dalším nepřítelem a utrpí zranění
    jdi(hráč, 'SZZ')
    zdraví = hráč.zdraví
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.zdraví < zdraví
    možnosti = zjisti_možné_akce(hráč)
    assert 'B' in možnosti
    assert not any(klávesa in možnosti for klávesa in 'SJZV')

    # pokusí se probít dál na západ
    while 'Z' not in zjisti_možné_akce(hráč):
        hráč.bojuj()
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
        assert hráč.žije(), 'K.I.A.'
    hráč.jdi_na_západ()

    # zkusí se trochu vyléčit
    for věc in hráč.inventář.copy():
        try:
            if věc.léčivá_síla <= 100 - hráč.zdraví:
                print(f'{věc}: {hráč.zdraví=}->', end='')
                hráč.spotřebuj(věc)
                print(hráč.zdraví)
        except AttributeError:
            continue

    # stojí na severo-jižní cestě poblíž vchodu do jeskyně
    assert (hráč.x, hráč.y) == (24, 20)

    # sebere další léčivku
    jdi(hráč, 'SZZSZ')
    počet_věcí = len(hráč.inventář)
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert len(hráč.inventář) == počet_věcí + 1
    assert hráč.inventář[-1].název.endswith(('houby', 'bobule', 'bylinky'))

    # dojde k mastičkáři, prodá nůž a dýku za 11 + 27
    jdi(hráč, 'VJVVSSS')
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

    # sebere další léčivku
    jdi(hráč, 'JJJJJJZZZJ')
    počet_věcí = len(hráč.inventář)
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert len(hráč.inventář) == počet_věcí + 1
    assert hráč.inventář[-1].název.endswith(('houby', 'bobule', 'bylinky'))

    # dojde na místo s dalším nepřítelem a utrpí zranění
    jdi(hráč, 'SS')
    zdraví = hráč.zdraví
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.zdraví < zdraví
    možnosti = zjisti_možné_akce(hráč)
    assert 'B' in možnosti
    assert not any(klávesa in možnosti for klávesa in 'SJZV')

    # pokusí se probít dál na sever
    while 'S' not in zjisti_možné_akce(hráč):
        hráč.bojuj()
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
        assert hráč.žije(), 'K.I.A.'
    hráč.jdi_na_sever()

    # zkusí se trochu vyléčit
    for věc in hráč.inventář.copy():
        try:
            if věc.léčivá_síla <= 100 - hráč.zdraví:
                print(f'{věc}: {hráč.zdraví=}->', end='')
                hráč.spotřebuj(věc)
                print(hráč.zdraví)
        except AttributeError:
            continue

    # sebere další léčivku
    jdi(hráč, 'ZZSZ')
    počet_věcí = len(hráč.inventář)
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert len(hráč.inventář) == počet_věcí + 1
    assert hráč.inventář[-1].název.endswith(('houby', 'bobule', 'bylinky'))

    # dojde na místo s lesním trollem a utrpí zranění
    jdi(hráč, 'VSS')
    zdraví = hráč.zdraví
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.zdraví < zdraví
    možnosti = zjisti_možné_akce(hráč)
    assert 'B' in možnosti
    assert not any(klávesa in možnosti for klávesa in 'SJZV')

    # pokusí se probít dál na sever
    while 'S' not in zjisti_možné_akce(hráč):
        hráč.bojuj()
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
        assert hráč.žije(), 'K.I.A.'
    hráč.jdi_na_sever()

    # zkusí se trochu vyléčit
    for věc in hráč.inventář.copy():
        try:
            if věc.léčivá_síla <= 100 - hráč.zdraví:
                print(f'{věc}: {hráč.zdraví=}->', end='')
                hráč.spotřebuj(věc)
                print(hráč.zdraví)
        except AttributeError:
            continue

    # dojde na místo s mečem a sebere ho
    jdi(hráč, 'ZZJZZJ')
    počet_věcí = len(hráč.inventář)
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert len(hráč.inventář) == počet_věcí + 1
    meč = hráč.inventář[-1]
    assert hráč.nejlepší_zbraň() is meč
    assert meč.název == 'Zrezivělý meč'

    # dojde na místo s dalším nepřítelem a utrpí zranění
    jdi(hráč, 'SZSS')
    zdraví = hráč.zdraví
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.zdraví < zdraví
    možnosti = zjisti_možné_akce(hráč)
    assert 'B' in možnosti
    assert not any(klávesa in možnosti for klávesa in 'SJZV')

    # pokusí se probít dál na východ
    while 'V' not in zjisti_možné_akce(hráč):
        hráč.bojuj()
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
        assert hráč.žije(), 'K.I.A.'
    hráč.jdi_na_východ()

    # sebere poslední léčivku v této části lesa
    hráč.jdi_na_východ()
    počet_věcí = len(hráč.inventář)
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert len(hráč.inventář) == počet_věcí + 1
    assert hráč.inventář[-1].název.endswith(('houby', 'bobule', 'bylinky'))

    # zkusí se trochu vyléčit
    for věc in hráč.inventář.copy():
        try:
            if věc.léčivá_síla <= 100 - hráč.zdraví:
                print(f'{věc}: {hráč.zdraví=}->', end='')
                hráč.spotřebuj(věc)
                print(hráč.zdraví)
        except AttributeError:
            continue

    # dojde na místo s nepřítelem a pokud ještě žije, zkusí přes něj přejít
    jdi(hráč, 'ZZ')
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    while 'J' not in zjisti_možné_akce(hráč):
        hráč.bojuj()
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
        assert hráč.žije(), 'K.I.A.'
    hráč.jdi_na_jih()

    # totéž udělá s dalším nepřítelem
    jdi(hráč, 'JVVVSVVJJJJVVJ')
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    while 'J' not in zjisti_možné_akce(hráč):
        hráč.bojuj()
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
        assert hráč.žije(), 'K.I.A.'
    hráč.jdi_na_jih()

    # dojde k mastičkáři, prodá sekerku za 45
    jdi(hráč, 'VVVSSSSSS')
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

    # zkusí se trochu vyléčit
    for věc in hráč.inventář.copy():
        try:
            if věc.léčivá_síla <= 100 - hráč.zdraví:
                print(f'{věc}: {hráč.zdraví=}->', end='')
                hráč.spotřebuj(věc)
                print(hráč.zdraví)
        except AttributeError:
            continue

    # dojde k prvnímu jeskynnímu nepříteli a utrpí zranění
    jdi(hráč, 'SSVSS')
    zdraví = hráč.zdraví
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.zdraví < zdraví
    možnosti = zjisti_možné_akce(hráč)
    assert 'B' in možnosti
    assert not any(klávesa in možnosti for klávesa in 'SJZV')

    # pokusí se probít dál na západ
    while 'Z' not in zjisti_možné_akce(hráč):
        hráč.bojuj()
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
        assert hráč.žije(), 'K.I.A.'
    hráč.jdi_na_západ()

    # vysbírá zlato v blízkém okolí
    jdi(hráč, 'SS')
    zlato = hráč.zlato
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.zlato > zlato
    jdi(hráč, 'JJZZJJ')
    zlato = hráč.zlato
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.zlato > zlato

    # dojde ke druhému jeskynnímu nepříteli a utrpí zranění
    jdi(hráč, 'SSSS')
    zdraví = hráč.zdraví
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.zdraví < zdraví
    možnosti = zjisti_možné_akce(hráč)
    assert 'B' in možnosti
    assert not any(klávesa in možnosti for klávesa in 'SJZV')

    # pokusí se probít dál na sever
    while 'S' not in zjisti_možné_akce(hráč):
        hráč.bojuj()
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
        assert hráč.žije(), 'K.I.A.'
    hráč.jdi_na_sever()

    # zkusí se trochu vyléčit
    for věc in hráč.inventář.copy():
        try:
            if věc.léčivá_síla <= 100 - hráč.zdraví:
                print(f'{věc}: {hráč.zdraví=}->', end='')
                hráč.spotřebuj(věc)
                print(hráč.zdraví)
        except AttributeError:
            continue

    # dojde na místo se zbraní (palcát, řemdih nebo mačeta) a sebere ji
    jdi(hráč, 'ZZJJJZ')
    počet_věcí = len(hráč.inventář)
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert len(hráč.inventář) == počet_věcí + 1
    zbraň_19x12 = hráč.inventář[-1]
    assert hráč.nejlepší_zbraň() is zbraň_19x12
    assert zbraň_19x12.název in ('Ostnatý palcát', 'Damascénská mačeta', 'Řemdih')

    # dojde na místo s nepřítelem a pokud ještě žije, zabije ho
    jdi(hráč, 'VSSSVVJ')
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    while hráč.místnost_pobytu().nepřítel.žije():
        hráč.bojuj()
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
        assert hráč.žije(), 'K.I.A.'
    hráč.jdi_na_jih()

    # totéž udělá s dalším nepřítelem
    jdi(hráč, 'JVVV')
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    while hráč.místnost_pobytu().nepřítel.žije():
        hráč.bojuj()
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
        assert hráč.žije(), 'K.I.A.'
    hráč.jdi_na_jih()

    # dojde k mastičkáři, prodá meč za 62
    jdi(hráč, 'JZJJ')
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

    # dojde k dalšímu nepříteli a utrpí zranění
    jdi(hráč, 'SSVSSZZZSSSZZJZZ')
    zdraví = hráč.zdraví
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.zdraví < zdraví
    možnosti = zjisti_možné_akce(hráč)
    assert 'B' in možnosti
    assert not any(klávesa in možnosti for klávesa in 'SJZV')

    # pokusí se probít dál na sever
    while 'S' not in zjisti_možné_akce(hráč):
        hráč.bojuj()
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
        assert hráč.žije(), 'K.I.A.'
    hráč.jdi_na_sever()

    # zkusí se trochu vyléčit
    for věc in hráč.inventář.copy():
        try:
            if věc.léčivá_síla <= 100 - hráč.zdraví:
                print(f'{věc}: {hráč.zdraví=}->', end='')
                hráč.spotřebuj(věc)
                print(hráč.zdraví)
        except AttributeError:
            continue

    # sebere zlato
    jdi(hráč, 'SZZ')
    zlato = hráč.zlato
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.zlato > zlato

    jdi(hráč, 'ZJJ')

    # stojí na křižovatce v pomyslném středu jeskyně
    assert (hráč.x, hráč.y) == (15, 10)

    # dojde k dalšímu nepříteli a utrpí zranění
    jdi(hráč, 'JJZ')
    zdraví = hráč.zdraví
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.zdraví < zdraví
    možnosti = zjisti_možné_akce(hráč)
    assert 'B' in možnosti
    assert not any(klávesa in možnosti for klávesa in 'SJZV')

    # pokusí se probít dál na západ
    while 'Z' not in zjisti_možné_akce(hráč):
        hráč.bojuj()
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
        assert hráč.žije(), 'K.I.A.'
    hráč.jdi_na_západ()

    # sebere zlato
    zlato = hráč.zlato
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.zlato > zlato

    # zkusí se trochu vyléčit
    for věc in hráč.inventář.copy():
        try:
            if věc.léčivá_síla <= 100 - hráč.zdraví:
                print(f'{věc}: {hráč.zdraví=}->', end='')
                hráč.spotřebuj(věc)
                print(hráč.zdraví)
        except AttributeError:
            continue

    # dojde pro nejbližší léčivku v druhém lese
    jdi(hráč, 'ZSSSZZZSZSZZS')
    počet_věcí = len(hráč.inventář)
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert len(hráč.inventář) == počet_věcí + 1
    assert hráč.inventář[-1].název.endswith(('houby', 'bobule', 'bylinky'))

    # dojde ke zbrojíři, prodá zbraň a koupí těžkou sekeru za 121
    jdi(hráč, 'JVVJV')
    assert 'O' in zjisti_možné_akce(hráč)

    zbrojíř = hráč.místnost_pobytu().obchodník
    sekera = next(věc for věc in zbrojíř.inventář if 'sekera' in věc.název)
    hráč.prodej(zbraň_19x12, zbrojíř)
    while hráč.zlato < sekera.cena and hráč.inventář:
        hráč.prodej(hráč.inventář[-1], zbrojíř)
    assert hráč.zlato >= 121, f'nejsou peníze na sekeru! ({hráč.zlato})'
    hráč.kup(sekera, zbrojíř)
    hráč.vypiš_věci()
