# coding: utf-8

from collections import OrderedDict
from typing import Dict, Tuple, Callable

from player import Player
from utils import color_print, print_game_title, print_action_name, nice_print
import world

ActionDict = Dict[str, Tuple[Callable, str]]


def get_available_actions(room, player) -> ActionDict:
    actions = OrderedDict()
    print('\nMožnosti:')
    try:
        enemy_near = room.enemy.is_alive()
    except AttributeError:
        enemy_near = False
    if enemy_near:
        action_adder(actions, 'B', player.attack, 'Bojovat\n')
    if not enemy_near or player.good_hit:
        player.good_hit = False
        if world.tile_at(room.x, room.y - 1):
            action_adder(actions, 'S', player.move_north, 'Jít na sever\t')
        if world.tile_at(room.x, room.y + 1):
            action_adder(actions, 'J', player.move_south, 'Jít na jih\t')
        if world.tile_at(room.x - 1, room.y):
            action_adder(actions, 'Z', player.move_west, 'Jít na západ\t')
        if world.tile_at(room.x + 1, room.y):
            action_adder(actions, 'V', player.move_east, 'Jít na východ')
        print()
    if isinstance(room, world.TraderTile):
        action_adder(actions, 'O', player.trade, 'Obchodovat\t')
    if player.hp < 100 and player.has_consumables():
        action_adder(actions, 'L', player.heal, 'Léčit se\t')
    action_adder(actions, 'I', player.print_info, 'Inventář\t')
    action_adder(actions, 'K', confirm_quit, 'Konec\n')
    color_print(f'[ Zdraví: {player.hp}\tzkušenost: {player.experience}'
                f'\tzlato: {player.gold} ]'.expandtabs(18), color='95')

    return actions


def action_adder(action_dict: ActionDict, hotkey, action: Callable, name):
    action_dict[hotkey] = action, name
    color_print(f'{hotkey}', end='', color='0')
    color_print(f': {name.expandtabs(15)}', end='', color='94')


def choose_action(room, player) -> Callable:
    available_actions = get_available_actions(room, player)
    print()

    while True:
        action_input = input('Co teď? ').upper()
        action, action_name = available_actions.get(action_input, (None, ''))
        if action is not None:
            print_action_name(action_name)
            return action
        else:
            color_print('?', color='95')


def confirm_quit():
    if input('Opravdu skončit? (A / cokoliv) ').upper() == 'A':
        quit_game()


def quit_game():
    raise SystemExit('Hra končí.')


def main():
    print_game_title()
    world.parse_world_dsl()
    player = Player()

    while True:
        room = world.tile_at(player.x, player.y)
        nice_print(room.intro_text())

        if isinstance(room, world.VictoryTile):
            break

        while True:
            room.modify_player(player)

            if not player.is_alive():
                quit_game()

            action = choose_action(room, player)
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
