# coding: utf-8

from player import Player
import utils


def main():
    utils.print_game_title()
    player = Player()
    command_buffer = []

    while True:
        utils.nice_print(player.current_room().intro_text())

        if player.is_winner():
            break

        while True:
            player.current_room().modify_player(player)

            if not player.is_alive():
                utils.quit_game()

            action = utils.choose_action(player, command_buffer)
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
        print('\nDokázal jsi to!',
              'Překonal jsi všechny nástrahy a získal poklad nesmírné ceny.',
              'Blahopřeji k vítězství.',
              sep='\n\n')
