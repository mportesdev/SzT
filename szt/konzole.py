# coding: utf-8

from itertools import chain
import random
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


def vypiš_úvodní_text(text):
    for odstavec in text:
        vypiš_odstavec(odstavec)


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


def vypiš_popis_místnosti(místnost):
    vypiš_odstavec(místnost.popis())


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


def vypiš_věc_v_obchodě(číslo_položky, věc, cena):
    print(f'{číslo_položky} ', end='')
    try:
        # ljust - kompenzovat 12 znaků za formátovací značky
        vypiš_barevně(
            f'{věc.název_4_pád} ([fialová]útok'
            f' +{věc.útok}[/]) '.ljust(ŠÍŘKA - 25 + 12, '.'),
            end=''
        )
    except AttributeError:
        # ljust - kompenzovat 11 znaků za formátovací značky
        vypiš_barevně(
            f'{věc.název_4_pád} ([tyrkys]zdraví'
            f' +{věc.léčivá_síla}[/]) '.ljust(ŠÍŘKA - 25 + 11, '.'),
            end=''
        )
    print(f' {cena:3} zlaťáků')


def vypiš_věc_k_léčení(číslo_položky, věc):
    vypiš_barevně(
        f'{číslo_položky:3}. {věc.název_7_pád} ('
        f'[tyrkys]zdraví +{věc.léčivá_síla}[/])'
    )


def vypiš_inventář(hráč):
    print('Máš u sebe:')
    for věc in chain(hráč.inventář, hráč.artefakty):
        vypiš_barevně('            ', věc, sep='')


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


def zpráva_o_útoku(zbraň, nepřítel):
    název_zbraně = zbraň.název_ve_větě if zbraň else 'pěsti'
    zpráva = (
        f'Použil jsi {název_zbraně} proti {nepřítel.jméno_3_pád.lower()}.'
    )
    if not nepřítel.žije():
        zpráva += f' Zabil jsi {nepřítel.jméno_4_pád.lower()}!'
    vypiš_odstavec(zpráva, 'boj')


def zpráva_zdařilý_zásah(nepřítel):
    vypiš_odstavec(
        f'Zasáhl jsi {nepřítel.jméno_4_pád.lower()} do hlavy.'
        f' {nepřítel.jméno} zmateně vrávorá.',
        'boj', 'modrá'
    )


def zpráva_o_zranění(hráč, nepřítel, zásah):
    zpráva = f'{nepřítel} útočí. '
    if hráč.žije():
        zpráva += ('Utrpěl jsi zranění.' if zásah > 0
                   else 'Ubránil ses.')
    else:
        zpráva += f'{random.choice(("Ouha", "Běda"))}, jsi mrtev!'
    vypiš_odstavec(zpráva, 'boj', 'červená')


def zpráva_kořist_zlato(nepřítel):
    vypiš_odstavec(f'Sebral jsi {nepřítel.jméno_3_pád.lower()}'
                   f' {nepřítel.zlato} zlaťáků.',
                   'štěstí')


def zpráva_kořist_zbraň(nepřítel):
    vypiš_odstavec(f'Sebral jsi {nepřítel.jméno_3_pád.lower()}'
                   f' {nepřítel.zbraň.název_4_pád.lower()}.',
                   'štěstí')
