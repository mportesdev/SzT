# coding: utf-8

import os
from textwrap import TextWrapper

GAME_TITLE = 'Strach ze tmy'
WIDTH = 72

INDENT_EMPTY = '            '
INDENT_INFO = '         🗨  '
INDENT_FIGHT = '         ⚔  '
INDENT_LUCK = '         ✰  '

text_wrapper = TextWrapper(width=WIDTH - len(INDENT_EMPTY),
                           subsequent_indent=INDENT_EMPTY)


def print_game_title():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\n\n' + ' '.join(GAME_TITLE).center(WIDTH) + '\n\n')


def print_action_name(action_name):
    print(f' {action_name.strip()} '.center(WIDTH, "-"), end='\n\n')


def nice_print(message, msg_type='info'):
    indent = dict(info=INDENT_INFO,
                  fight=INDENT_FIGHT,
                  luck=INDENT_LUCK).get(msg_type, INDENT_EMPTY)
    text_wrapper.initial_indent = indent
    for line in message.splitlines():
        print(text_wrapper.fill(line))
