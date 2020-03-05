# coding: utf-8

from player import Hráč
import utils


def hra():
    utils.zobraz_titul()
    hráč = Hráč()
    fronta_příkazů = []

    while True:
        místnost = hráč.místnost_pobytu()
        utils.vypiš_odstavec(místnost.popis())

        if not místnost.navštívena:
            fronta_příkazů.clear()

            místnost.navštívena = True
            if hráč.svět.vše_navštíveno():
                utils.uděl_odměnu(hráč, 100, 'prozkoumání všech míst')
            if místnost is hráč.svět.začátek:
                utils.vypiš_odstavec(
                    'Svou rodnou vesnici, stejně jako vcelku poklidný život'
                    ' pekařského učedníka, jsi nechal daleko za sebou a vydal'
                    ' ses na nejistou dráhu dobrodruha.'
                )
                utils.vypiš_odstavec(
                    'Uvnitř pověstmi opředené hory se prý ukrývá pětice'
                    ' posvátných magických předmětů, které i obyčejnému'
                    ' smrtelníkovi mohou přinést nadlidské schopnosti.'
                )

        if místnost is hráč.svět.začátek and hráč.svět.poklad_posbírán():
            break

        while True:
            místnost.dopad_na_hráče(hráč)

            if not hráč.žije():
                raise SystemExit

            akce = utils.vyber_akci(hráč, fronta_příkazů)
            akce()

            # v případě pohybu vyskočit do vnější smyčky a vypsat popis
            # místnosti
            if akce in (hráč.jdi_na_sever, hráč.jdi_na_jih,
                        hráč.jdi_na_východ, hráč.jdi_na_západ):
                break

    print('\nDokázal jsi to!\n\nBlahopřeji k vítězství.')


if __name__ == '__main__':
    try:
        hra()
    except SystemExit:
        print('\nHra končí.')
