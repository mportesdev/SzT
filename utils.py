# coding: utf-8

import os
import random
import sys
from textwrap import TextWrapper
import time

GAME_TITLE = 'Strach ze tmy'
WIDTH = 70
DELAY = 0.025

INDENT_EMPTY = '           '
INDENT_INFO = '        >  '
INDENT_FIGHT = '        !  '
INDENT_LUCK = '        *  '

text_wrapper = TextWrapper(width=WIDTH - len(INDENT_EMPTY),
                           subsequent_indent=INDENT_EMPTY)


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
                'verze 0.5, 13. ledna 2020'.center(WIDTH),
                '\n\n',
                sep='\n',
                color='1;95')
    color_print('-' * WIDTH, end='\n\n', color='95')


def print_action_name(action_name):
    color_print(f' {action_name.strip()} '.center(WIDTH, '-'), end='\n\n',
                color='95')


def nice_print(message, msg_type='info', color=None):
    indent = dict(info=INDENT_INFO,
                  fight=INDENT_FIGHT,
                  luck=INDENT_LUCK).get(msg_type, INDENT_EMPTY)
    text_wrapper.initial_indent = indent
    color_print(text_wrapper.fill(message), color=color)


def oscillate(number, relative_delta=0.2):
    delta = int(number * relative_delta)
    return random.randint(number - delta, number + delta)


if '--no-color' in sys.argv[1:] or os.name == 'nt':
    color_print = color_print_dummy
