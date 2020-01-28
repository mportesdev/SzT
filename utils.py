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
DELAY = 0.025

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


def print_game_title():
    os.system('cls' if os.name == 'nt' else 'clear')
    color_print('\n\n',
                ' '.join(GAME_TITLE).center(WIDTH),
                '\n',
                'textová hra na hrdiny'.center(WIDTH),
                '',
                'verze 0.7, 28. ledna 2020'.center(WIDTH),
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
            print(f'{hotkey}', end='')
            name = available_actions[hotkey][1]
            if hotkey == hotkey_group[-1]:
                color_print(f': {name}', color=BLUE)
            else:
                color_print(f': {name:<15}', end='', color=BLUE)


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
        if player.world.tile_at(room.x, room.y - 1):
            actions['S'] = (player.move_north, 'Jít na sever')
        if player.world.tile_at(room.x, room.y + 1):
            actions['J'] = (player.move_south, 'Jít na jih')
        if player.world.tile_at(room.x - 1, room.y):
            actions['Z'] = (player.move_west, 'Jít na západ')
        if player.world.tile_at(room.x + 1, room.y):
            actions['V'] = (player.move_east, 'Jít na východ')

    if player.hp < 100 and player.has_consumables():
        actions['L'] = (player.heal, 'Léčit se')

    actions['I'] = (player.print_inventory, 'Inventář')
    actions['K'] = (confirm_quit, 'Konec')

    return actions


def choose_action(player, command_buffer):
    while True:
        available_actions = get_available_actions(player)
        if not command_buffer:
            print_options(available_actions)
            color_print(f'[ Zdraví: {player.hp}\tzkušenost: {player.xp}'
                        f'\tzlato: {player.gold} ]'.expandtabs(18),
                        color=MAGENTA)
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


def oscillate(number, relative_delta=0.2):
    delta = int(number * relative_delta)
    return random.randint(number - delta, number + delta)


def hotkey_groups(hotkeys):
    return re.search(r'([BO]*)([SJZV]*)([LIK]*)', hotkeys).groups()


def confirm_quit():
    if input('Opravdu skončit? (A / cokoliv) ').upper() == 'A':
        quit_game()


def quit_game():
    print('\nHra končí.')
    raise SystemExit


if '--no-color' in sys.argv[1:] or (os.name == 'nt'
                                    and '--color' not in sys.argv[1:]):
    color_print = color_print_dummy
