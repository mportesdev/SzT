# coding: utf-8

from collections import OrderedDict
from textwrap import TextWrapper

from player import Player
import world

WIDTH = 72
INDENT_EMPTY = '            '
INDENT_INFO = '         🗨  '
INDENT_FIGHT = '         ⚔  '
INDENT_LUCK = '         ✰  '


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
    action_adder(actions, 'K', quit_game, 'Konec\n')

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
            print(f' {action_name.strip()} '.center(WIDTH, "-"), end='\n\n')
            action()
            return
        else:
            print('?')


def quit_game():
    raise SystemExit('Hra končí.')


def main():
    text_wrapper = TextWrapper(width=WIDTH - len(INDENT_EMPTY),
                               initial_indent=INDENT_INFO,
                               subsequent_indent=INDENT_EMPTY)
    print('\n\n' + 'S t r a c h   z e   t m y'.center(WIDTH) + '\n\n')
    world.parse_world_dsl()
    player = Player()

    while player.is_alive() and not player.victory:
        room = world.tile_at(player.x, player.y)
        for line in room.intro_text().splitlines():
            print(text_wrapper.fill(line))
        auto_message = room.modify_player(player)
        if auto_message:
            if isinstance(room, world.EnemyTile):
                indent = INDENT_FIGHT
            elif isinstance(room, (world.FindGoldTile, world.FindWeaponTile)):
                indent = INDENT_LUCK
            else:
                indent = INDENT_EMPTY
            print(f'\n{indent}{auto_message}')

        if player.is_alive() and not player.victory:
            choose_action(room, player)
        elif not player.is_alive():
            print('Jsi mrtev.')
            quit_game()


if __name__ == '__main__':
    try:
        main()
    except SystemExit as err:
        print(err)
    else:
        print('Blahopřeji.')
