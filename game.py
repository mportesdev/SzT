# coding: utf-8

from collections import OrderedDict

from player import Player
from utils import color_print, print_game_title, print_action_name, nice_print
import world


def get_available_actions(room, player):
    actions = OrderedDict()
    print('\nMožnosti:')
    if isinstance(room, world.EnemyTile) and room.enemy.is_alive():
        action_adder(actions, 'B', player.attack, 'Bojovat')
    else:
        if world.tile_at(room.x, room.y - 1):
            action_adder(actions, 'S', player.move_north, 'Jít na sever\t')
        if world.tile_at(room.x, room.y + 1):
            action_adder(actions, 'J', player.move_south, 'Jít na jih\t')
        if world.tile_at(room.x + 1, room.y):
            action_adder(actions, 'V', player.move_east, 'Jít na východ\t')
        if world.tile_at(room.x - 1, room.y):
            action_adder(actions, 'Z', player.move_west, 'Jít na západ')
    print()
    if isinstance(room, world.TraderTile):
        action_adder(actions, 'O', player.trade, 'Obchodovat\t')
    if player.hp < 100 and player.has_consumables():
        action_adder(actions, 'L', player.heal, 'Léčit se\t')
    action_adder(actions, 'I', player.print_info, 'Informace\t')
    action_adder(actions, 'K', confirm_quit, 'Konec\n')

    return actions


def action_adder(action_dict, hotkey, action, name):
    action_dict[hotkey] = action, name
    color_print(f'{hotkey}: {name.expandtabs(16)}', end='', color=4)


def choose_action(room, player):
    available_actions = get_available_actions(room, player)
    print()

    while True:
        action_input = input('Co teď? ').upper()
        action, action_name = available_actions.get(action_input, (None, ''))
        if action is not None:
            print_action_name(action_name)
            return action
        else:
            color_print('?', color=6)


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
