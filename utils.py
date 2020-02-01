# coding: utf-8

from collections import OrderedDict
import os
import random
import re
import sys
from textwrap import TextWrapper
import time

GAME_TITLE = 'Strach ze tmy'
WIDTH = 70
DELAY = 0.015

# Colors
NONE = '0'
RED = '91'
BLUE = '94'
MAGENTA = '95'
CYAN = '96'

INDENT_EMPTY = '           '
INDENT_INFO = '        >  '
INDENT_FIGHT = '        !  '
INDENT_LUCK = '        *  '

text_wrapper = TextWrapper(width=WIDTH - len(INDENT_EMPTY),
                           subsequent_indent=INDENT_EMPTY)


def nice_print(message, msg_type='info', color=None):
    indent = dict(info=INDENT_INFO,
                  fight=INDENT_FIGHT,
                  luck=INDENT_LUCK).get(msg_type, INDENT_EMPTY)
    text_wrapper.initial_indent = indent
    color_print(text_wrapper.fill(message), color=color)


def color_print(*args, color=None, **kwargs):
    if color is not None:
        print(f'\033[{color}m', end='')

    print(*args, **kwargs)

    if color is not None:
        print('\033[0m', end='')
    time.sleep(DELAY)


def color_print_dummy(*args, color=None, **kwargs):
    print(*args, **kwargs)
    time.sleep(DELAY)


def multicolor(text, colors, delimiter='|', end='\n'):
    split_text = text.split(delimiter)
    item_count = len(split_text)
    color_count = len(colors)

    if item_count > color_count:
        raise ValueError(f'Not enough color information (expected {item_count},'
                         f' got {color_count})')

    for item, color in zip(split_text, colors):
        color_print(item, color=color, end='')
    print(end=end)


def print_game_title():
    os.system('cls' if os.name == 'nt' else 'clear')
    color_print('\n\n',
                ' '.join(GAME_TITLE).center(WIDTH),
                '\n',
                'textová hra na hrdiny'.center(WIDTH),
                '',
                'verze 0.8, 30. ledna 2020'.center(WIDTH),
                '\n\n',
                sep='\n',
                color=MAGENTA)
    color_print('-' * WIDTH, end='\n\n', color=MAGENTA)


def print_action_name(action_name):
    color_print(f' {action_name.strip()} '.center(WIDTH, '-'), end='\n\n',
                color=MAGENTA)


def print_options(available_actions):
    print('\nMožnosti:')
    for hotkey_group in hotkey_groups(''.join(available_actions.keys())):
        for hotkey in hotkey_group:
            name = available_actions[hotkey][1]
            if hotkey == hotkey_group[-1]:
                multicolor(f'{hotkey}|: {name}', (NONE, BLUE))
            else:
                multicolor(f'{hotkey}|: {name:<15}', (NONE, BLUE), end='')


def award_bonus(player, bonus, achievement):
    player.xp += bonus
    nice_print(f'Za {achievement} získáváš zkušenost {bonus} bodů!',
               color=MAGENTA)


def get_available_actions(player):
    room = player.current_room()
    actions = OrderedDict()

    try:
        enemy_near = room.enemy.is_alive()
    except AttributeError:
        enemy_near = False
    if enemy_near:
        actions['B'] = (player.attack, 'Bojovat')

    if hasattr(room, 'trader'):
        actions['O'] = (player.trade, 'Obchodovat')

    if not enemy_near or player.good_hit:
        player.good_hit = False

        room_north = player.world.tile_at(room.x, room.y - 1)
        room_south = player.world.tile_at(room.x, room.y + 1)
        room_west = player.world.tile_at(room.x - 1, room.y)
        room_east = player.world.tile_at(room.x + 1, room.y)

        if room_north:
            actions['S'] = (player.move_north, 'Jít na sever')
            room_north.seen = True
        if room_south:
            actions['J'] = (player.move_south, 'Jít na jih')
            room_south.seen = True
        if room_west:
            actions['Z'] = (player.move_west, 'Jít na západ')
            room_west.seen = True
        if room_east:
            actions['V'] = (player.move_east, 'Jít na východ')
            room_east.seen = True

    if player.hp < 100 and player.has_consumables():
        actions['L'] = (player.heal, 'Léčit se')

    actions['I'] = (player.print_inventory, 'Inventář')
    actions['M'] = (player.print_map, 'Mapa')
    actions['K'] = (confirm_quit, 'Konec')

    return actions


def choose_action(player, command_buffer):
    while True:
        available_actions = get_available_actions(player)
        if not command_buffer:
            print_options(available_actions)
            multicolor(f'[ Zdraví: |{player.hp:<8}|zkušenost: |{player.xp:<7}|'
                       f'zlato: |{player.gold:<4}|]',
                       (MAGENTA, NONE, MAGENTA, NONE, MAGENTA, NONE, MAGENTA))
            print()

        while True:
            if command_buffer:
                action_input = command_buffer.pop(0)
                if action_input not in available_actions:
                    command_buffer.clear()
                    break
            else:
                action_input = input('Co teď? ').upper()
                if set(action_input).issubset(set('SJZV')):
                    command_buffer.extend(action_input[1:])
                    action_input = action_input[:1]
            action, action_name = available_actions.get(action_input,
                                                        (None, ''))
            if action is not None:
                print_action_name(action_name)
                return action
            else:
                command_buffer.clear()
                color_print('?', color=MAGENTA)


def option_input(options):
    while True:
        user_input = input()
        for option in options:
            if user_input == str(option):
                return option
        else:
            color_print('?', color=MAGENTA)


def oscillate(number, relative_delta=0.2):
    delta = int(number * relative_delta)
    return random.randint(number - delta, number + delta)


def hotkey_groups(hotkeys):
    return re.search(r'([BO]*)([SJZV]*)([LIMK]*)', hotkeys).groups()


def leading_trailing(input_str, value):
    pattern = f'^({value}*).*?({value}*)$'
    leading, trailing = re.match(pattern, input_str).groups()

    return len(leading), len(trailing)


def confirm_quit():
    if input('Opravdu skončit? (A / cokoliv) ').upper() == 'A':
        quit_game()


def quit_game():
    print('\nHra končí.')
    raise SystemExit


if '--no-color' in sys.argv[1:] or (os.name == 'nt'
                                    and '--color' not in sys.argv[1:]):
    color_print = color_print_dummy
