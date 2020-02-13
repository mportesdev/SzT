# coding: utf-8

from player import Player
import utils


def main():
    utils.print_game_title()
    player = Player()
    command_buffer = []

    while True:
        room = player.current_room()
        utils.nice_print(room.intro_text())

        if not room.visited:
            command_buffer.clear()

            room.visited = True
            if player.world.all_tiles_visited():
                utils.award_bonus(player, 100, 'prozkoumání všech míst')
            if room is player.world.start_tile:
                utils.nice_print('Svou rodnou vesnici, stejně'
                                 ' jako vcelku poklidný život pekařského'
                                 ' učedníka, jsi nechal daleko za sebou a'
                                 ' vydal ses na nejistou dráhu dobrodruha.',
                                 'none')
                utils.nice_print('Uvnitř pověstmi opředené hory se prý ukrývá'
                                 ' pětice posvátných magických předmětů, které'
                                 ' i obyčejnému smrtelníkovi mohou přinést'
                                 ' nadlidské schopnosti.')

        if player.is_winner():
            break

        while True:
            room.modify_player(player)

            if not player.is_alive():
                raise SystemExit

            action = utils.choose_action(player, command_buffer)
            action()

            # if the player moves, break to the outer loop to print
            # the room description
            if action in (player.move_north, player.move_south,
                          player.move_east, player.move_west):
                break

    print('\nDokázal jsi to!\n\nBlahopřeji k vítězství.')


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        print('\nHra končí.')
