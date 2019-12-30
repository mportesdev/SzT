# coding: utf-8

from textwrap import TextWrapper

GAME_TITLE = 'Strach ze tmy'
WIDTH = 72

INDENT_EMPTY = '            '
INDENT_INFO = '         🗨  '
INDENT_FIGHT = '         ⚔  '
INDENT_LUCK = '         ✰  '

text_wrapper = TextWrapper(width=WIDTH - len(INDENT_EMPTY),
                           initial_indent=INDENT_INFO,
                           subsequent_indent=INDENT_EMPTY)


def print_game_title():
    print('\n\n' + ' '.join(GAME_TITLE).center(WIDTH) + '\n\n')


def print_action_name(action_name):
    print(f' {action_name.strip()} '.center(WIDTH, "-"), end='\n\n')


def print_wrapped(text):
    for line in text.splitlines():
        print(text_wrapper.fill(line))


def nice_print(message, msg_type):
    indent = dict(fight=INDENT_FIGHT,
                  luck=INDENT_LUCK).get(msg_type, INDENT_EMPTY)
    print(f'\n{indent}{message}')
