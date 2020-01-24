# coding: utf-8

from collections import OrderedDict
import re
from typing import Dict, Tuple, Callable

from player import Player
from utils import color_print, print_game_title, print_action_name, nice_print

ActionDict = Dict[str, Tuple[Callable, str]]


def get_available_actions(player) -> ActionDict:
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


def choose_action(player, command_buffer: list) -> Callable:
    while True:
        available_actions = get_available_actions(player)
        if not command_buffer:
            print_options(available_actions)
            color_print(f'[ Zdraví: {player.hp}\tzkušenost: {player.experience}'
                        f'\tzlato: {player.gold} ]'.expandtabs(18), color='95')
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
                color_print('?', color='95')


def print_options(available_actions):
    print('\nMožnosti:')
    hotkeys = ''.join(available_actions.keys())
    hotkey_groups = re.search(r'([BO]*)([SJZV]*)([LIK]*)', hotkeys).groups()

    for hotkey_group in hotkey_groups:
        for hotkey in hotkey_group:
            print(f'{hotkey}', end='')
            name = available_actions[hotkey][1]
            if hotkey == hotkey_group[-1]:
                color_print(f': {name}', color='94')
            else:
                color_print(f': {name:<15}', end='', color='94')


def confirm_quit():
    if input('Opravdu skončit? (A / cokoliv) ').upper() == 'A':
        quit_game()


def quit_game():
    raise SystemExit('Hra končí.')


def main():
    print_game_title()
    player = Player()
    command_buffer = []

    while True:
        nice_print(player.current_room().intro_text())

        if player.is_winner():
            break

        while True:
            player.current_room().modify_player(player)

            if not player.is_alive():
                quit_game()

            action = choose_action(player, command_buffer)
            action()

            # if the player moves, break to the outer loop to print
            # the room description
            if action in (player.move_north, player.move_south,
                          player.move_east, player.move_west):
                break


if __name__ == '__main__':
    try:
        main()
    except SystemExit as err:
        print(err)
    else:
        print('\n\nDokázal jsi to! Blahopřeji k vítězství.')
