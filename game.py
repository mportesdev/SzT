# coding: utf-8

from player import Hráč
import utils


def main():
    utils.print_game_title()
    hráč = Hráč()
    command_buffer = []

    while True:
        room = hráč.místnost_pobytu()
        utils.nice_print(room.intro_text())

        if not room.visited:
            command_buffer.clear()

            room.visited = True
            if hráč.svět.all_tiles_visited():
                utils.award_bonus(hráč, 100, 'prozkoumání všech míst')
            if room is hráč.svět.start_tile:
                utils.nice_print('Svou rodnou vesnici, stejně'
                                 ' jako vcelku poklidný život pekařského'
                                 ' učedníka, jsi nechal daleko za sebou a'
                                 ' vydal ses na nejistou dráhu dobrodruha.')
                utils.nice_print('Uvnitř pověstmi opředené hory se prý ukrývá'
                                 ' pětice posvátných magických předmětů, které'
                                 ' i obyčejnému smrtelníkovi mohou přinést'
                                 ' nadlidské schopnosti.')

        if room is hráč.svět.start_tile \
                and hráč.svět.treasure_collected():
            break

        while True:
            room.modify_player(hráč)

            if not hráč.žije():
                raise SystemExit

            action = utils.choose_action(hráč, command_buffer)
            action()

            # if the player moves, break to the outer loop to print
            # the room description
            if action in (hráč.jdi_na_sever, hráč.jdi_na_jih,
                          hráč.jdi_na_východ, hráč.jdi_na_západ):
                break

    print('\nDokázal jsi to!\n\nBlahopřeji k vítězství.')


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        print('\nHra končí.')
