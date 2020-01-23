# coding: utf-8

from collections import OrderedDict
from typing import Dict, Tuple, Callable

from player import Player
from utils import color_print, print_game_title, print_action_name, nice_print

ActionDict = Dict[str, Tuple[Callable, str]]

movement_hotkeys = {'S', 'J', 'Z', 'V'}


def get_available_actions(player) -> ActionDict:
    room = player.current_room()
    actions = OrderedDict()
    try:
        enemy_near = room.enemy.is_alive()
    except AttributeError:
        enemy_near = False
    if enemy_near:
        actions['B'] = (player.attack, 'Bojovat\n')
    if not enemy_near or player.good_hit:
        player.good_hit = False
        if player.world.tile_at(room.x, room.y - 1):
            actions['S'] = (player.move_north, 'Jít na sever\t')
        if player.world.tile_at(room.x, room.y + 1):
            actions['J'] = (player.move_south, 'Jít na jih\t')
        if player.world.tile_at(room.x - 1, room.y):
            actions['Z'] = (player.move_west, 'Jít na západ\t')
        if player.world.tile_at(room.x + 1, room.y):
            actions['V'] = (player.move_east, 'Jít na východ')
    if hasattr(room, 'trader'):
        actions['O'] = (player.trade, 'Obchodovat\t')
    if player.hp < 100 and player.has_consumables():
        actions['L'] = (player.heal, 'Léčit se\t')
    actions['I'] = (player.print_inventory, 'Inventář\t')
    actions['K'] = (confirm_quit, 'Konec\n')

    return actions


def choose_action(player, command_buffer) -> Callable:
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
                first = False
            else:
                action_input = input('Co teď? ').upper()
                if set(action_input).issubset(movement_hotkeys):
                    command_buffer.extend(action_input[1:])
                    player.fast_travel = bool(command_buffer)
                    action_input = action_input[:1]
                    first = True
            action, action_name = available_actions.get(action_input,
                                                        (None, ''))
            if action is not None:
                print_action_name(action_name)
                return action
            else:
                command_buffer.clear()
                if player.fast_travel and not first:
                    break
                else:
                    color_print('?', color='95')


def print_options(available_actions):
    print('\nMožnosti:')
    movements = [k for k in available_actions.keys() if k in movement_hotkeys]

    for hotkey, (_, name) in available_actions.items():
        color_print(f'{hotkey}', end='', color='0')
        color_print(f': {name.expandtabs(15)}', end='', color='94')
        if movements and hotkey == movements[-1]:
            print()


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
        # if not player.fast_travel:
        #     nice_print(player.current_room().intro_text())
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
