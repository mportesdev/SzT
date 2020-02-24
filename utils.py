# coding: utf-8

from collections import OrderedDict
from enum import Enum
from itertools import cycle
import os
import random
import re
import sys
from textwrap import TextWrapper
import time

NÁZEV_HRY = 'Strach ze tmy'
ŠÍŘKA = 70
PRODLEVA = 0.015


class DarkColor(Enum):
    RED = 31
    BLUE = 34
    MAGENTA = 35
    CYAN = 36


class BrightColor(Enum):
    RED = 91
    BLUE = 94
    MAGENTA = 95
    CYAN = 96


ODSAZENÍ = ' ' * 11

zalamovač_textu = TextWrapper(width=ŠÍŘKA - len(ODSAZENÍ),
                              subsequent_indent=ODSAZENÍ)


def vypiš_odstavec(zpráva, typ_zprávy='info', barva=None):
    symbol = dict(info='>', boj='!', štěstí='*').get(typ_zprávy, ' ')
    zalamovač_textu.initial_indent = f'        {symbol}  '

    if typ_zprávy == 'štěstí' and barva is None:
        barva = Color.CYAN

    vypiš_barevně(zalamovač_textu.fill(zpráva), barva=barva)


def vypiš_barevně(*args, barva=None, **kwargs):
    if barva is not None:
        print(f'\033[{barva.value}m', end='')

    print(*args, **kwargs)

    if barva is not None:
        print('\033[0m', end='')
    time.sleep(PRODLEVA)


def color_print_dummy(*args, color=None, **kwargs):
    print(*args, **kwargs)
    time.sleep(PRODLEVA)


def multicolor(text, colors, repeat=True, delimiter='|', end='\n'):
    text_items = text.split(delimiter)

    if repeat:
        colors = cycle(colors)
    else:
        if len(text_items) > len(colors):
            raise ValueError('Not enough color information (expected at least'
                             f' {len(text_items)}, got {len(colors)})')

    for item, color in zip(text_items, colors):
        vypiš_barevně(item, barva=color, end='')
    print(end=end)


def print_game_title():
    os.system('cls' if os.name == 'nt' else 'clear')
    vypiš_barevně('\n\n',
                  ' '.join(NÁZEV_HRY).center(ŠÍŘKA),
                  '\n',
                  'textová hra na hrdiny'.center(ŠÍŘKA),
                  '',
                  'verze 0.8, 30. ledna 2020'.center(ŠÍŘKA),
                  '\n\n',
                  barva=Color.MAGENTA, sep='\n')
    vypiš_barevně('-' * ŠÍŘKA, barva=Color.MAGENTA, end='\n\n')


def print_action_name(action_name):
    vypiš_barevně(f' {action_name.strip()} '.center(ŠÍŘKA, '-'),
                  barva=Color.MAGENTA, end='\n\n')


def print_options(available_actions):
    print('\nMožnosti:')
    for hotkey_group in hotkey_groups(''.join(available_actions.keys())):
        for hotkey in hotkey_group:
            name = available_actions[hotkey][1]
            if hotkey == hotkey_group[-1]:
                multicolor(f'{hotkey}|: {name}', (None, Color.BLUE))
            else:
                multicolor(f'{hotkey}|: {name:<15}', (None, Color.BLUE), end='')


def uděl_odměnu(hráč, odměna, za_co):
    hráč.xp += odměna
    vypiš_odstavec(f'Za {za_co} získáváš zkušenost {odměna} bodů!',
                   barva=Color.MAGENTA)


def get_available_actions(player):
    room = player.místnost_pobytu()
    actions = OrderedDict()

    try:
        enemy_near = room.nepřítel.žije()
    except AttributeError:
        enemy_near = False
    if enemy_near:
        actions['B'] = (player.bojuj, 'Bojovat')

    if hasattr(room, 'obchodník'):
        actions['O'] = (player.obchoduj, 'Obchodovat')

    if not enemy_near or player.zdařilý_zásah:
        player.zdařilý_zásah = False

        room_north = player.svět.místnost_na_pozici(room.x, room.y - 1)
        room_south = player.svět.místnost_na_pozici(room.x, room.y + 1)
        room_west = player.svět.místnost_na_pozici(room.x - 1, room.y)
        room_east = player.svět.místnost_na_pozici(room.x + 1, room.y)

        if room_north:
            actions['S'] = (player.jdi_na_sever, 'Jít na sever')
            room_north.viděna = True
        if room_south:
            actions['J'] = (player.jdi_na_jih, 'Jít na jih')
            room_south.viděna = True
        if room_west:
            actions['Z'] = (player.jdi_na_západ, 'Jít na západ')
            room_west.viděna = True
        if room_east:
            actions['V'] = (player.jdi_na_východ, 'Jít na východ')
            room_east.viděna = True

    if player.zdraví < 100 and player.má_léčivky():
        actions['L'] = (player.kurýruj_se, 'Léčit se')

    actions['I'] = (player.vypiš_věci, 'Inventář')
    actions['M'] = (player.nakresli_mapu, 'Mapa')
    actions['K'] = (confirm_quit, 'Konec')

    return actions


def vyber_akci(hráč, fronta_příkazů):
    while True:
        dostupné_akce = get_available_actions(hráč)
        if not fronta_příkazů:
            print_options(dostupné_akce)
            multicolor(f'[ Zdraví: |{hráč.zdraví:<8}|'
                       f'zkušenost: |{hráč.xp:<7}|'
                       f'zlato: |{hráč.zlato}| ]', (Color.MAGENTA, None))
            print()

        while True:
            if fronta_příkazů:
                vstup = fronta_příkazů.pop(0)
                if vstup not in dostupné_akce:
                    fronta_příkazů.clear()
                    break
            else:
                vstup = input('Co teď? ').upper()
                if set(vstup).issubset(set('SJZV')):
                    fronta_příkazů.extend(vstup[1:])
                    vstup = vstup[:1]
            akce, název_akce = dostupné_akce.get(vstup, (None, ''))
            if akce is not None:
                print_action_name(název_akce)
                return akce
            else:
                fronta_příkazů.clear()
                vypiš_barevně('?', barva=Color.MAGENTA)


def option_input(options, ignore_case=True):
    while True:
        user_input = input()
        for option in options:
            if user_input == str(option) or \
                    ignore_case and user_input.upper() == str(option).upper():
                return option
        else:
            vypiš_barevně('?', barva=Color.MAGENTA)


def oscillate(number, relative_delta=0.2):
    delta = int(number * relative_delta)
    return random.randint(number - delta, number + delta)


def hotkey_groups(hotkeys):
    return re.search(r'([BO]*)([SJZV]*)([LIMK]*)', hotkeys).groups()


def okolí(input_str, value):
    pattern = f'^({value}*).*?({value}*)$'
    leading, trailing = re.match(pattern, input_str).groups()

    return len(leading), len(trailing)


def confirm_quit():
    multicolor('Opravdu skončit? (|A| / |N|)', (Color.BLUE, None), end=' ')
    if option_input({'A', 'N'}) == 'A':
        raise SystemExit


Color = DarkColor if '--dark' in sys.argv[1:] else BrightColor

if '--no-color' in sys.argv[1:] or (os.name == 'nt'
                                    and '--color' not in sys.argv[1:]):
    color_print = color_print_dummy
