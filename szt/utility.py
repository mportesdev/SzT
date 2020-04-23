# coding: utf-8

from collections import OrderedDict
import random
import re

from . import dialogy, konzole


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

        místnost_severně = hráč.svět.místnost_na_pozici(místnost.x,
                                                        místnost.y - 1)
        místnost_jižně = hráč.svět.místnost_na_pozici(místnost.x,
                                                      místnost.y + 1)
        místnost_západně = hráč.svět.místnost_na_pozici(místnost.x - 1,
                                                        místnost.y)
        místnost_východně = hráč.svět.místnost_na_pozici(místnost.x + 1,
                                                         místnost.y)

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

    akce['I'] = (hráč.vypiš_věci, 'Inventář')

    if not hráč.mapování and len(set(akce) & set('SJZV')) > 2:
        # na první křižovatce si hráč začne dělat mapu
        hráč.mapování = True

    if hráč.mapování:
        akce['M'] = (hráč.nakresli_mapu, 'Mapa')

    akce['K'] = (dialogy.potvrď_konec, 'Konec')

    return akce


def vyber_akci(hráč, fronta_příkazů):
    while True:
        možnosti = zjisti_možné_akce(hráč)
        if not fronta_příkazů:
            konzole.zobraz_možnosti(možnosti)
            konzole.vypiš_barevně('[ Zdraví:', barva='fialová', end='')
            konzole.vypiš_barevně(f' {hráč.zdraví:3} {"%":<4}'
                                  f'[fialová]zkušenost:[/] {hráč.zkušenost:<7}'
                                  f'[fialová]zlato:[/] {hráč.zlato} '
                                  '[fialová]]')
            print()

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
                konzole.vypiš_název_akce(název_akce)
                return akce
            else:
                fronta_příkazů.clear()
                konzole.vypiš_barevně('?', barva='fialová')


def s_odchylkou(číslo, relativní_odchylka=0.2):
    odchylka = int(číslo * relativní_odchylka)
    return random.randint(číslo - odchylka, číslo + odchylka)


def okraje(řetězec, hodnota_okraje):
    vzorec = f'^({hodnota_okraje}*).*?({hodnota_okraje}*)$'
    levý_okraj, pravý_okraj = re.match(vzorec, řetězec).groups()

    return len(levý_okraj), len(pravý_okraj)
