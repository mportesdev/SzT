# coding: utf-8

from collections import OrderedDict

from player import Player
from utils import print_game_title, print_action_name, print_wrapped
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
    print(f'{hotkey}: {name.expandtabs(16)}', end='')


def choose_action(room, player):
    available_actions = get_available_actions(room, player)
    print()

    while True:
        action_input = input('Co teď? ').upper()
        action, action_name = available_actions.get(action_input, (None, ''))
        if action:
            print_action_name(action_name)
            action()
            return
        else:
            print('?')


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
        print_wrapped(room.intro_text())

        if isinstance(room, world.VictoryTile):
            break

        room.modify_player(player)

        if not player.is_alive():
            print('Jsi mrtev.')
            quit_game()

        choose_action(room, player)


if __name__ == '__main__':
    try:
        main()
    except SystemExit as err:
        print(err)
    else:
        print('\n\nDokázal jsi to! Blahopřeji k vítězství.')
