# coding: utf-8

import re
import sys
import time
from textwrap import TextWrapper

from rich.console import Console

from . import barvy

NÁZEV_HRY = 'Strach ze tmy'
VERZE = '1.1'

RYCHLE = '-R' in sys.argv[1:]
DÉLKA_PRODLEVY = 0.015

ŠÍŘKA = 70
ODSAZENÍ = ' ' * 11

zalamovač_textu = TextWrapper(width=ŠÍŘKA - len(ODSAZENÍ),
                              subsequent_indent=ODSAZENÍ)

konzole = Console(theme=barvy.barevný_motiv)


def vypiš_odstavec(zpráva, typ_zprávy='info', barva=None):
    symbol = dict(info='>', boj='!', štěstí='*').get(typ_zprávy, ' ')
    zalamovač_textu.initial_indent = f'        {symbol}  '

    if typ_zprávy == 'štěstí' and barva is None:
        barva = 'tyrkys'

    vypiš_barevně(zalamovač_textu.fill(zpráva), barva=barva)


def vypiš_barevně(*args, barva=None, **kwargs):
    konzole.print(*args, style=barva, highlight=False, **kwargs)
    if not RYCHLE:
        time.sleep(DÉLKA_PRODLEVY)


def zobraz_titul():
    vypiš_barevně('-' * ŠÍŘKA, barva='fialová')
    vypiš_barevně(
        '\n\n',
        ' '.join(NÁZEV_HRY).center(ŠÍŘKA),
        '\n\n\n',
        'textová hra na hrdiny'.center(ŠÍŘKA),
        '\n\n',
        f'verze {VERZE}   21. dubna 2020'.center(ŠÍŘKA),
        '\n\n',
        barva='fialová', sep='')
    vypiš_barevně('-' * ŠÍŘKA, barva='fialová', end='\n\n')


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
    vypiš_barevně(
        f'{NÁZEV_HRY}       verze {VERZE}       '
        'github.com/myrmica-habilis/SzT.git'.center(ŠÍŘKA),
        barva='fialová')
    vypiš_barevně('-' * ŠÍŘKA, barva='fialová')


def nerozumím():
    vypiš_barevně('?', barva='fialová')


def vypiš_název_akce(název_akce):
    vypiš_barevně(f' {název_akce} '.center(ŠÍŘKA, '-'),
                  barva='fialová', end='\n\n')


def nakresli_mapu(svět, pozice_hráče):
    print('\n'.join(''.join(řádka).center(ŠÍŘKA)
                    for řádka in svět.mapa_navštívených(pozice_hráče)))
    print()
    legenda_mapy()


def legenda_mapy():
    vypiš_barevně('[', barva='modrá', end='')
    vypiš_barevně(' + [modrá]les[/]           # '
                  '[modrá]jeskyně[/]         H [modrá]hráč[/]'
                  '            ? [modrá]neznámo ]')


def stav_hráče(hráč):
    vypiš_barevně('[ Zdraví:', barva='fialová', end='')
    vypiš_barevně(f' {hráč.zdraví:3} {"%":<4}'
                  f'[fialová]zkušenost:[/] {hráč.zkušenost:<7}'
                  f'[fialová]zlato:[/] {hráč.zlato} '
                  '[fialová]]')


def zobraz_možnosti(možnosti):
    print('\nMožnosti:')
    for skupina_kláves in skupiny_kláves(''.join(možnosti.keys())):
        for klávesa in skupina_kláves:
            název = možnosti[klávesa][1]
            if klávesa == skupina_kláves[-1]:
                vypiš_barevně(f'{klávesa}[modrá]: {název}')
            else:
                vypiš_barevně(f'{klávesa}[modrá]: {název:<15}', end='')


def skupiny_kláves(klávesy):
    return re.search(r'([BO]*)([SJZV]*)([LIMK]*)', klávesy).groups()


def uděl_odměnu(hráč, odměna, za_co):
    hráč.zkušenost += odměna
    vypiš_odstavec(f'Za {za_co} získáváš zkušenost {odměna} bodů!',
                   barva='fialová')
