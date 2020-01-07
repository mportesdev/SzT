# coding: utf-8

import os
import sys
from textwrap import TextWrapper

GAME_TITLE = 'Strach ze tmy'
WIDTH = 70

INDENT_EMPTY = '           '
INDENT_INFO = '        🗨  '
INDENT_FIGHT = '        ⚔  '
INDENT_LUCK = '        ★  '

text_wrapper = TextWrapper(width=WIDTH - len(INDENT_EMPTY),
                           subsequent_indent=INDENT_EMPTY)


def color_print(*args, color=None, **kwargs):
    if color is not None:
        print(f'\033[{color}m', end='')

    print(*args, **kwargs)

    if color is not None:
        print('\033[0m', end='')


def color_print_dummy(*args, color=None, **kwargs):
    print(*args, **kwargs)


def print_game_title():
    os.system('cls' if os.name == 'nt' else 'clear')
    color_print('\n\n' + ' '.join(GAME_TITLE).center(WIDTH) + '\n\n',
                color='1;95')


def print_action_name(action_name):
    color_print(f' {action_name.strip()} '.center(WIDTH, "-"), end='\n\n',
                color='95')


def nice_print(message, msg_type='info', color=None):
    indent = dict(info=INDENT_INFO,
                  fight=INDENT_FIGHT,
                  luck=INDENT_LUCK).get(msg_type, INDENT_EMPTY)
    text_wrapper.initial_indent = indent
    color_print(text_wrapper.fill(message), color=color)


for arg in sys.argv[1:]:
    if arg in ('--no-color', '-c'):
        color_print = color_print_dummy
    elif arg in ('--no-symbols', '-s'):
        INDENT_INFO = INDENT_INFO.replace('🗨', '>')
        INDENT_FIGHT = INDENT_FIGHT.replace('⚔', '!')
        INDENT_LUCK = INDENT_LUCK.replace('★', '*')
