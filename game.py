# coding: utf-8

from collections import OrderedDict
from textwrap import TextWrapper

from player import Player
import world

WIDTH = 66
INDENT = '  '


def get_available_actions(room, player):
    actions = OrderedDict()
    print("\nMožnosti:")
    if isinstance(room, world.EnemyTile) and room.enemy.is_alive():
        action_adder(actions, 'B', player.attack, "Bojovat")
    else:
        if world.tile_at(room.x, room.y - 1):
            action_adder(actions, 'S', player.move_north, "Jít na sever")
        if world.tile_at(room.x, room.y + 1):
            action_adder(actions, 'J', player.move_south, "Jít na jih")
        if world.tile_at(room.x + 1, room.y):
            action_adder(actions, 'V', player.move_east, "Jít na východ")
        if world.tile_at(room.x - 1, room.y):
            action_adder(actions, 'Z', player.move_west, "Jít na západ")
    if player.inventory:
        action_adder(actions, 'I', player.print_inventory, "Inventář")
    if isinstance(room, world.TraderTile):
        action_adder(actions, 'O', player.trade, "Obchodovat")
    if player.hp < 100 and player.has_consumables():
        action_adder(actions, 'L', player.heal, "Léčit se")
    action_adder(actions, 'K', quit_game, "Konec")

    return actions


def action_adder(action_dict, hotkey, action, name):
    action_dict[hotkey] = action
    # TODO: display all options on 2 or 3 lines
    print(f"{hotkey}: {name}")


def choose_action(room, player):
    action = None
    while not action:
        available_actions = get_available_actions(room, player)
        action_input = input("Co teď? ").upper()
        action = available_actions.get(action_input)
        if action:
            print('O.K.\n')
            action()
        else:
            print("Nerozumím.\n")


def quit_game():
    raise SystemExit('Hra končí.')


def main():
    text_wrapper = TextWrapper(width=WIDTH - len(INDENT),
                               initial_indent=INDENT,
                               subsequent_indent=INDENT)
    print('\n', 'S t r a c h   z e   t m y'.center(WIDTH), '\n')
    world.parse_world_dsl()
    player = Player()

    while player.is_alive() and not player.victory:
        room = world.tile_at(player.x, player.y)
        print('-' * WIDTH)
        for line in room.intro_text().splitlines():
            print(text_wrapper.fill(line))
        print('-' * WIDTH)
        room.modify_player(player)

        if player.is_alive() and not player.victory:
            choose_action(room, player)
        elif not player.is_alive():
            print("Jsi mrtev.")
            quit_game()


if __name__ == '__main__':
    try:
        main()
    except SystemExit as err:
        print(err)
    else:
        print('Blahopřeji.')
