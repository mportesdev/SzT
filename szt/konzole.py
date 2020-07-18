# coding: utf-8

from itertools import chain
import random
import re
import sys
import time
from textwrap import TextWrapper

from rich.console import Console
from rich.text import Text

from . import barvy

NÁZEV_HRY = 'Strach ze tmy'
VERZE = '1.2'
DATUM = '18. července 2020'

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

    piš(zalamovač_textu.fill(zpráva), barva=barva)


def piš(*args, barva=None, **kwargs):
    konzole.print(*args, style=barva, highlight=False, **kwargs)
    if not RYCHLE:
        time.sleep(DÉLKA_PRODLEVY)


def zobraz_titul():
    piš('-' * ŠÍŘKA, barva='fialová')
    piš('\n\n',
        ' '.join(NÁZEV_HRY).center(ŠÍŘKA),
        '\n\n\n',
        'textová hra na hrdiny'.center(ŠÍŘKA),
        '\n\n',
        f'verze {VERZE}   {DATUM}'.center(ŠÍŘKA),
        '\n\n',
        barva='fialová', sep='')
    piš('-' * ŠÍŘKA, barva='fialová', end='\n\n')


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
    piš('\n\n',
        'Dokázal jsi to! Blahopřeji k vítězství.'.center(ŠÍŘKA),
        '\n\n',
        sep='')
    piš(
        f'{NÁZEV_HRY}       verze {VERZE}       '
        'github.com/myrmica-habilis/SzT.git'.center(ŠÍŘKA),
        barva='fialová')
    piš('-' * ŠÍŘKA, barva='fialová')


def nerozumím():
    piš('?', barva='fialová')


def vypiš_název_akce(název_akce):
    piš(f' {název_akce} '.center(ŠÍŘKA, '-'),
        barva='fialová', end='\n\n')


def vypiš_popis_místnosti(místnost):
    vypiš_odstavec(místnost.popis())


def nakresli_mapu(svět, pozice_hráče):
    mapa = Text('\n'.join(''.join(řádka).center(ŠÍŘKA)
                          for řádka in svět.mapa_navštívených(pozice_hráče)))
    nastav_barvy_mapy(mapa)
    piš(mapa)
    piš()
    legenda_mapy()


def legenda_mapy():
    legenda = Text(
        '[ + les           # jeskyně         H hráč            ? neznámo ]'
    )
    nastav_barvy_mapy(legenda)
    piš(legenda)


def nastav_barvy_mapy(text: Text):
    for regex, barva in (
            (r'[^H]+', 'modrá'),
            (r'#+', 'fialová'),
            (r'\++', 'tyrkys'),
    ):
        text.highlight_regex(regex, barva)


def stav_hráče(hráč):
    piš('[ Zdraví:', barva='fialová', end='')
    piš(f' {hráč.zdraví:3} {"%":<4}'
        f'[fialová]zkušenost:[/] {hráč.zkušenost:<7}'
        f'[fialová]zlato:[/] {hráč.zlato} '
        '[fialová]]', end='\n\n')


def vypiš_věc_v_obchodě(číslo_položky, věc, cena):
    piš(f'{číslo_položky:3}. ' if číslo_položky else '     ', end='')
    popis_věci = f'{věc:4}'

    # vypočítat délku formátovacích značek [fialová][/], resp. [tyrkys][/]
    délka_značek = len(''.join(re.findall(r'\[.*?\]', popis_věci)))

    # ljust - kompenzovat formátovací značky
    piš((popis_věci + ' ').ljust(ŠÍŘKA - 25 + délka_značek, '.'), end='')

    piš(f' {cena:3} zlaťáků')


def vypiš_věc_k_léčení(číslo_položky, věc):
    piš(f'{číslo_položky:3}. {věc:7}')


def vypiš_inventář(hráč):
    if not hráč.inventář and not hráč.artefakty:
        piš('Nic u sebe nemáš.')
        return

    piš('Máš u sebe:')
    for věc in chain(hráč.inventář, hráč.artefakty):
        piš(f'            {věc:4}')


def zobraz_možnosti(možnosti):
    piš('\nMožnosti:')
    for skupina_kláves in skupiny_kláves(''.join(možnosti.keys())):
        for klávesa in skupina_kláves:
            název = možnosti[klávesa][1]
            if klávesa == skupina_kláves[-1]:
                piš(f'{klávesa}[modrá]: {název}')
            else:
                piš(f'{klávesa}[modrá]: {název:<15}', end='')


def skupiny_kláves(klávesy):
    return re.search(r'([BO]*)([SJZV]*)([LIMK]*)', klávesy).groups()


def zpráva_o_odměně(za_co, kolik):
    vypiš_odstavec(f'Za {za_co} získáváš zkušenost {kolik} bodů!',
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
