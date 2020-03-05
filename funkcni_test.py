from player import Hráč
from utils import zjisti_možné_akce


def test_zakladni_pruchod_hrou():
    hráč = Hráč()

    # hráč stojí na začátku, je zdráv, má u sebe dvě věci, zatím si nedělá mapu
    # TODO: aktivace mapy az na prvni krizovatce
    assert (hráč.x, hráč.y) == (hráč.svět.začátek.x, hráč.svět.začátek.y)
    assert hráč.zdraví == 100
    assert len(hráč.inventář) == 2
    # assert set(zjisti_možné_akce(hráč).keys()) == set('SIK')

    # jde dál lesem
    hráč.jdi_na_sever()
    hráč.jdi_na_sever()
    # assert set(zjisti_možné_akce(hráč).keys()) == set('SJIK')

    # dojde na první křižovatku a rozhodne se kreslit mapu
    hráč.jdi_na_sever()
    assert set(zjisti_možné_akce(hráč).keys()) == set('SJZIMK')

    # dojde na místo s bylinkami a sebere je
    hráč.jdi_na_sever()
    hráč.jdi_na_východ()
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert len(hráč.inventář) == 3
    assert 'bylinky' in hráč.inventář[-1].název
    assert set(zjisti_možné_akce(hráč).keys()) == set('ZIMK')

    # dojde na místo s nepřítelem a utrpí zranění
    hráč.jdi_na_západ()
    hráč.jdi_na_jih()
    hráč.jdi_na_západ()
    hráč.jdi_na_západ()
    hráč.jdi_na_sever()
    hráč.jdi_na_západ()
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.zdraví < 100
    assert set(zjisti_možné_akce(hráč).keys()) == set('BLIMK')

    # pokusí se probít dál na západ
    while 'Z' not in zjisti_možné_akce(hráč):
        hráč.bojuj()
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.žije()
    hráč.jdi_na_západ()

    # dojde na místo s dýkou a sebere ji
    hráč.jdi_na_západ()
    hráč.jdi_na_západ()
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert len(hráč.inventář) == 4
    assert 'dýka' in hráč.inventář[-1].název

    # zkusí se trochu vyléčit
    for věc in hráč.inventář.copy():
        try:
            if věc.léčivá_síla <= 100 - hráč.zdraví:
                print(f'{věc}: {hráč.zdraví=}->', end='')
                hráč.zdraví += věc.léčivá_síla
                print(hráč.zdraví)
                hráč.inventář.remove(věc)
        except AttributeError:
            continue

    # dojde na místo s houbami a sebere je
    hráč.jdi_na_východ()
    hráč.jdi_na_jih()
    hráč.jdi_na_jih()
    hráč.jdi_na_východ()
    hráč.jdi_na_východ()
    počet_věcí = len(hráč.inventář)
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert len(hráč.inventář) == počet_věcí + 1
    assert 'houby' in hráč.inventář[-1].název
    assert set(zjisti_možné_akce(hráč).keys()) == set('ZLIMK')

    # dojde na místo s dalším nepřítelem a utrpí zranění
    hráč.jdi_na_západ()
    hráč.jdi_na_západ()
    hráč.jdi_na_sever()
    hráč.jdi_na_sever()
    hráč.jdi_na_východ()
    hráč.jdi_na_sever()
    hráč.jdi_na_sever()
    hráč.jdi_na_východ()
    hráč.jdi_na_východ()
    hráč.jdi_na_sever()
    zdraví = hráč.zdraví
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.zdraví < zdraví
    assert set(zjisti_možné_akce(hráč).keys()) == set('BLIMK')

    # pokusí se probít dál na sever
    while 'S' not in zjisti_možné_akce(hráč):
        hráč.bojuj()
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.žije()
    hráč.jdi_na_sever()

    # dojde na místo s bobulemi a sebere je
    hráč.jdi_na_sever()
    počet_věcí = len(hráč.inventář)
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert len(hráč.inventář) == počet_věcí + 1
    assert 'bobule' in hráč.inventář[-1].název

    # zkusí se trochu vyléčit
    for věc in hráč.inventář.copy():
        try:
            if věc.léčivá_síla <= 100 - hráč.zdraví:
                print(f'{věc}: {hráč.zdraví=}->', end='')
                hráč.zdraví += věc.léčivá_síla
                print(hráč.zdraví)
                hráč.inventář.remove(věc)
        except AttributeError:
            continue

    # dojde na místo s další léčivkou a sebere ji
    hráč.jdi_na_jih()
    hráč.jdi_na_západ()
    hráč.jdi_na_západ()
    hráč.jdi_na_sever()
    hráč.jdi_na_západ()
    hráč.jdi_na_západ()
    hráč.jdi_na_jih()
    hráč.jdi_na_jih()
    hráč.jdi_na_jih()
    počet_věcí = len(hráč.inventář)
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert len(hráč.inventář) == počet_věcí + 1

    # dojde na místo s dalším nepřítelem a utrpí zranění
    hráč.jdi_na_sever()
    hráč.jdi_na_západ()
    hráč.jdi_na_západ()
    zdraví = hráč.zdraví
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.zdraví < zdraví
    assert set(zjisti_možné_akce(hráč).keys()) == set('BLIMK')

    # pokusí se probít dál na západ
    while 'Z' not in zjisti_možné_akce(hráč):
        hráč.bojuj()
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.žije()
    hráč.jdi_na_západ()

    # zkusí se trochu vyléčit
    for věc in hráč.inventář.copy():
        try:
            if věc.léčivá_síla <= 100 - hráč.zdraví:
                print(f'{věc}: {hráč.zdraví=}->', end='')
                hráč.zdraví += věc.léčivá_síla
                print(hráč.zdraví)
                hráč.inventář.remove(věc)
        except AttributeError:
            continue

    # stojí na severo-jižní cestě poblíž vchodu do jeskyně
    assert (hráč.x, hráč.y) == (24, 20)

    # dojde k obchodníkovi pro sekerku
    # TODO

    # sebere další dvě léčivky v okolí
    hráč.jdi_na_sever()
    hráč.jdi_na_západ()
    hráč.jdi_na_západ()
    hráč.jdi_na_sever()
    hráč.jdi_na_západ()
    počet_věcí = len(hráč.inventář)
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert len(hráč.inventář) == počet_věcí + 1

    hráč.jdi_na_východ()
    hráč.jdi_na_jih()
    hráč.jdi_na_východ()
    hráč.jdi_na_východ()
    hráč.jdi_na_jih()
    hráč.jdi_na_jih()
    hráč.jdi_na_jih()
    hráč.jdi_na_západ()
    hráč.jdi_na_západ()
    hráč.jdi_na_západ()
    hráč.jdi_na_jih()
    počet_věcí = len(hráč.inventář)
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert len(hráč.inventář) == počet_věcí + 1

    # dojde na místo s dalším nepřítelem a utrpí zranění
    hráč.jdi_na_sever()
    hráč.jdi_na_sever()
    zdraví = hráč.zdraví
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.zdraví < zdraví
    assert set(zjisti_možné_akce(hráč).keys()) == set('BLIMK')

    # pokusí se probít dál na sever
    while 'S' not in zjisti_možné_akce(hráč):
        hráč.bojuj()
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.žije()
    hráč.jdi_na_sever()

    # zkusí se trochu vyléčit
    for věc in hráč.inventář.copy():
        try:
            if věc.léčivá_síla <= 100 - hráč.zdraví:
                print(f'{věc}: {hráč.zdraví=}->', end='')
                hráč.zdraví += věc.léčivá_síla
                print(hráč.zdraví)
                hráč.inventář.remove(věc)
        except AttributeError:
            continue

    # sebere další léčivku
    hráč.jdi_na_západ()
    hráč.jdi_na_západ()
    hráč.jdi_na_sever()
    hráč.jdi_na_západ()
    počet_věcí = len(hráč.inventář)
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert len(hráč.inventář) == počet_věcí + 1

    # dojde na místo s lesním trollem a utrpí zranění
    hráč.jdi_na_východ()
    hráč.jdi_na_sever()
    hráč.jdi_na_sever()
    zdraví = hráč.zdraví
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.zdraví < zdraví
    assert set(zjisti_možné_akce(hráč).keys()) == set('BLIMK')

    # pokusí se probít dál na sever
    while 'S' not in zjisti_možné_akce(hráč):
        hráč.bojuj()
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.žije()
    hráč.jdi_na_sever()

    # zkusí se trochu vyléčit
    for věc in hráč.inventář.copy():
        try:
            if věc.léčivá_síla <= 100 - hráč.zdraví:
                print(f'{věc}: {hráč.zdraví=}->', end='')
                hráč.zdraví += věc.léčivá_síla
                print(hráč.zdraví)
                hráč.inventář.remove(věc)
        except AttributeError:
            continue

    # dojde na místo s mečem a sebere ho
    hráč.jdi_na_západ()
    hráč.jdi_na_západ()
    hráč.jdi_na_jih()
    hráč.jdi_na_západ()
    hráč.jdi_na_západ()
    hráč.jdi_na_jih()
    počet_věcí = len(hráč.inventář)
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert len(hráč.inventář) == počet_věcí + 1
    assert 'meč' in hráč.inventář[-1].název

    # dojde na místo s dalším nepřítelem a utrpí zranění
    hráč.jdi_na_sever()
    hráč.jdi_na_západ()
    hráč.jdi_na_sever()
    hráč.jdi_na_sever()
    zdraví = hráč.zdraví
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.zdraví < zdraví
    assert set(zjisti_možné_akce(hráč).keys()) == set('BIMK')

    # pokusí se probít dál na východ
    while 'V' not in zjisti_možné_akce(hráč):
        hráč.bojuj()
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.žije()
    hráč.jdi_na_východ()

    # sebere poslední léčivku v této části lesa
    hráč.jdi_na_východ()
    počet_věcí = len(hráč.inventář)
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert len(hráč.inventář) == počet_věcí + 1

    # zkusí se trochu vyléčit
    for věc in hráč.inventář.copy():
        try:
            if věc.léčivá_síla <= 100 - hráč.zdraví:
                print(f'{věc}: {hráč.zdraví=}->', end='')
                hráč.zdraví += věc.léčivá_síla
                print(hráč.zdraví)
                hráč.inventář.remove(věc)
        except AttributeError:
            continue

    # dojde na místo s nepřítelem a pokud ještě žije, zkusí přes něj přejít
    hráč.jdi_na_západ()
    hráč.jdi_na_západ()
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    while 'J' not in zjisti_možné_akce(hráč):
        hráč.bojuj()
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.žije()
    hráč.jdi_na_jih()

    # totéž udělá s dalším nepřítelem
    hráč.jdi_na_jih()
    hráč.jdi_na_východ()
    hráč.jdi_na_východ()
    hráč.jdi_na_východ()
    hráč.jdi_na_sever()
    hráč.jdi_na_východ()
    hráč.jdi_na_východ()
    hráč.jdi_na_jih()
    hráč.jdi_na_jih()
    hráč.jdi_na_jih()
    hráč.jdi_na_jih()
    hráč.jdi_na_východ()
    hráč.jdi_na_východ()
    hráč.jdi_na_jih()
    hráč.místnost_pobytu().dopad_na_hráče(hráč)
    while 'J' not in zjisti_možné_akce(hráč):
        hráč.bojuj()
        hráč.místnost_pobytu().dopad_na_hráče(hráč)
    assert hráč.žije()
    hráč.jdi_na_jih()

    # dojde k mastičkáři a sekerku zase prodá
    hráč.jdi_na_východ()
    hráč.jdi_na_východ()
    hráč.jdi_na_východ()
    hráč.jdi_na_sever()
    hráč.jdi_na_sever()
    hráč.jdi_na_sever()
    hráč.jdi_na_sever()
    hráč.jdi_na_sever()
    hráč.jdi_na_sever()
    assert set(zjisti_možné_akce(hráč).keys()) == set('OSJIMK')
    # TODO
