# coding: utf-8

from collections import OrderedDict

from . import agent, data, hrac


def zjisti_možné_akce(hráč):
    místnost = hráč.místnost_pobytu()
    akce = OrderedDict()

    try:
        nepřítel_poblíž = místnost.nepřítel.žije()
    except AttributeError:
        nepřítel_poblíž = False
    if nepřítel_poblíž:
        akce['B'] = (hráč.bojuj, 'Bojovat')

    if hasattr(místnost, 'obchodník'):
        akce['O'] = (hráč.obchoduj, 'Obchodovat')

    if not nepřítel_poblíž or hráč.zdařilý_zásah:
        hráč.zdařilý_zásah = False

        místnost_severně = hráč.svět[místnost.x, místnost.y - 1]
        místnost_jižně = hráč.svět[místnost.x, místnost.y + 1]
        místnost_západně = hráč.svět[místnost.x - 1, místnost.y]
        místnost_východně = hráč.svět[místnost.x + 1, místnost.y]

        if místnost_severně:
            akce['S'] = (hráč.jdi_na_sever, 'Jít na sever')
            místnost_severně.viděna = True
        if místnost_jižně:
            akce['J'] = (hráč.jdi_na_jih, 'Jít na jih')
            místnost_jižně.viděna = True
        if místnost_západně:
            akce['Z'] = (hráč.jdi_na_západ, 'Jít na západ')
            místnost_západně.viděna = True
        if místnost_východně:
            akce['V'] = (hráč.jdi_na_východ, 'Jít na východ')
            místnost_východně.viděna = True

    if (hráč.zdraví < 100 and hráč.má_léky()) \
            or any(věc.speciální for věc in hráč.inventář
                   if hasattr(věc, 'speciální')):
        akce['L'] = (hráč.kurýruj_se, 'Léčit se')

    akce['I'] = (hráč.vypiš_inventář, 'Inventář')

    if not hráč.mapování and len(set(akce) & set('SJZV')) > 2:
        # na první křižovatce si hráč začne dělat mapu
        hráč.mapování = True

    if hráč.mapování:
        akce['M'] = (hráč.nakresli_mapu, 'Mapa')

    akce['K'] = (agent.potvrď_konec, 'Konec')

    return akce


def vyber_akci(hráč, fronta_příkazů):
    while True:
        možnosti = zjisti_možné_akce(hráč)
        if not fronta_příkazů:
            agent.zobraz_možnosti(možnosti)
            agent.stav_hráče(hráč)

        while True:
            if fronta_příkazů:
                vstup = fronta_příkazů.pop(0)
                if vstup not in možnosti:
                    fronta_příkazů.clear()
                    break
            else:
                vstup = input('Co teď? ').upper()
                if set(vstup).issubset(set('SJZV')):
                    fronta_příkazů.extend(vstup[1:])
                    vstup = vstup[:1]
            akce, název_akce = možnosti.get(vstup, (None, ''))
            if akce is not None:
                agent.vypiš_název_akce(název_akce)
                return akce
            else:
                fronta_příkazů.clear()
                agent.nerozumím()


def hra():
    agent.zobraz_titul()
    hráč = hrac.Hráč()
    fronta_příkazů = []

    while True:
        místnost = hráč.místnost_pobytu()
        agent.vypiš_popis_místnosti(místnost)

        if not místnost.navštívena:
            fronta_příkazů.clear()

            místnost.navštívena = True
            if hráč.svět.vše_navštíveno():
                agent.uděl_odměnu(hráč, 100, 'prozkoumání všech míst')
            if místnost is hráč.svět.začátek:
                agent.vypiš_úvodní_text(data.úvodní_text)

        if místnost is hráč.svět.začátek and hráč.svět.poklad_posbírán():
            agent.zobraz_gratulaci()
            break

        while True:
            místnost.dopad_na_hráče(hráč)

            if not hráč.žije():
                raise SystemExit

            akce = vyber_akci(hráč, fronta_příkazů)
            akce()

            # v případě pohybu vyskočit do vnější smyčky a vypsat popis
            # místnosti
            if akce in (hráč.jdi_na_sever, hráč.jdi_na_jih,
                        hráč.jdi_na_východ, hráč.jdi_na_západ):
                break
