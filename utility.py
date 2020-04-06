# coding: utf-8

from collections import OrderedDict
from enum import Enum
from itertools import cycle
import random
import re
import sys
from textwrap import TextWrapper
import time

NÁZEV_HRY = 'Strach ze tmy'
VERZE = 'verze 1.0'
ŠÍŘKA = 70


class TmaváBarva(Enum):
    ČERVENÁ = 31
    MODRÁ = 34
    FIALOVÁ = 35
    TYRKYS = 36


class SvětláBarva(Enum):
    ČERVENÁ = 91
    MODRÁ = 94
    FIALOVÁ = 95
    TYRKYS = 96


ODSAZENÍ = ' ' * 11

zalamovač_textu = TextWrapper(width=ŠÍŘKA - len(ODSAZENÍ),
                              subsequent_indent=ODSAZENÍ)


def vypiš_odstavec(zpráva, typ_zprávy='info', barva=None):
    symbol = dict(info='>', boj='!', štěstí='*').get(typ_zprávy, ' ')
    zalamovač_textu.initial_indent = f'        {symbol}  '

    if typ_zprávy == 'štěstí' and barva is None:
        barva = Barva.TYRKYS

    vypiš_barevně(zalamovač_textu.fill(zpráva), barva=barva)


def vypiš_barevně(*args, barva=None, **kwargs):
    if barva is not None:
        print(f'\033[{barva.value}m', end='')

    print(*args, **kwargs)

    if barva is not None:
        print('\033[0m', end='')
    time.sleep(PRODLEVA)


def vypiš_barevně_atrapa(*args, barva=None, **kwargs):
    print(*args, **kwargs)
    time.sleep(PRODLEVA)


def vícebarevně(text, barvy, oddělovač='|', konec='\n'):
    části_textu = text.split(oddělovač)
    barvy = cycle(barvy)

    for část, barva in zip(části_textu, barvy):
        vypiš_barevně(část, barva=barva, end='')
    print(end=konec)


def zobraz_titul():
    vypiš_barevně('-' * ŠÍŘKA, barva=Barva.FIALOVÁ)
    vypiš_barevně('\n\n',
                  ' '.join(NÁZEV_HRY).center(ŠÍŘKA),
                  '\n\n\n',
                  'textová hra na hrdiny'.center(ŠÍŘKA),
                  '\n\n',
                  f'{VERZE}   6. dubna 2020'.center(ŠÍŘKA),
                  '\n\n',
                  barva=Barva.FIALOVÁ, sep='')
    vypiš_barevně('-' * ŠÍŘKA, barva=Barva.FIALOVÁ, end='\n\n')


def zobraz_gratulaci():
    vypiš_odstavec('Překonal jsi všechny nástrahy a s notnou dávkou odvahy i'
                   ' štěstí se ti skutečně podařilo získat kýžené magické'
                   ' artefakty.',
                   'štěstí')
    vypiš_odstavec('Otevírá se před tebou svět takřka neomezených možností.'
                   ' Bude záležet jen na tobě, zda se staneš mocným mágem na'
                   ' straně dobra, anebo zla.')
    print('\n\n',
          'Dokázal jsi to! Blahopřeji k vítězství.'.center(ŠÍŘKA),
          '\n\n',
          sep='')
    vypiš_barevně(f'{NÁZEV_HRY}       {VERZE}       '
                  'github.com/myrmica-habilis/SzT.git'.center(ŠÍŘKA),
                  barva=Barva.FIALOVÁ)
    vypiš_barevně('-' * ŠÍŘKA, barva=Barva.FIALOVÁ)


def vypiš_název_akce(název_akce):
    vypiš_barevně(f' {název_akce} '.center(ŠÍŘKA, '-'),
                  barva=Barva.FIALOVÁ, end='\n\n')


def zobraz_možnosti(možnosti):
    print('\nMožnosti:')
    for skupina_kláves in skupiny_kláves(''.join(možnosti.keys())):
        for klávesa in skupina_kláves:
            název = možnosti[klávesa][1]
            if klávesa == skupina_kláves[-1]:
                vícebarevně(f'{klávesa}|: {název}', (None, Barva.MODRÁ))
            else:
                vícebarevně(f'{klávesa}|: {název:<15}', (None, Barva.MODRÁ),
                            konec='')


def uděl_odměnu(hráč, odměna, za_co):
    hráč.zkušenost += odměna
    vypiš_odstavec(f'Za {za_co} získáváš zkušenost {odměna} bodů!',
                   barva=Barva.FIALOVÁ)


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

    akce['K'] = (potvrď_konec, 'Konec')

    return akce


def vyber_akci(hráč, fronta_příkazů):
    while True:
        možnosti = zjisti_možné_akce(hráč)
        if not fronta_příkazů:
            zobraz_možnosti(možnosti)
            vícebarevně(f'[ Zdraví: |{hráč.zdraví:3} {"%":<4}|'
                        f'zkušenost: |{hráč.zkušenost:<7}|'
                        f'zlato: |{hráč.zlato}| ]', (Barva.FIALOVÁ, None))
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
                vypiš_název_akce(název_akce)
                return akce
            else:
                fronta_příkazů.clear()
                vypiš_barevně('?', barva=Barva.FIALOVÁ)


def vstup_z_možností(možnosti):
    while True:
        vstup = input()
        for možnost in možnosti:
            if vstup.upper() == str(možnost).upper():
                return možnost
        else:
            vypiš_barevně('?', barva=Barva.FIALOVÁ)


def s_odchylkou(číslo, relativní_odchylka=0.2):
    odchylka = int(číslo * relativní_odchylka)
    return random.randint(číslo - odchylka, číslo + odchylka)


def skupiny_kláves(klávesy):
    return re.search(r'([BO]*)([SJZV]*)([LIMK]*)', klávesy).groups()


def okraje(řetězec, hodnota_okraje):
    vzorec = f'^({hodnota_okraje}*).*?({hodnota_okraje}*)$'
    levý_okraj, pravý_okraj = re.match(vzorec, řetězec).groups()

    return len(levý_okraj), len(pravý_okraj)


def potvrď_konec():
    vícebarevně('Opravdu skončit? (|A| / |N|)', (Barva.MODRÁ, None), konec=' ')
    if vstup_z_možností({'A', 'N'}) == 'A':
        raise SystemExit


Barva = TmaváBarva if '--dark' in sys.argv[1:] else SvětláBarva

if '--no-color' in sys.argv[1:] or (sys.platform == 'win32'
                                    and '--color' not in sys.argv[1:]):
    vypiš_barevně = vypiš_barevně_atrapa

PRODLEVA = 0 if '--fast' in sys.argv[1:] else 0.015
