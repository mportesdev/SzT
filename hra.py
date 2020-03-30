# coding: utf-8

from hrac import Hráč
import utility


def hra():
    utility.zobraz_titul()
    hráč = Hráč()
    fronta_příkazů = []

    while True:
        místnost = hráč.místnost_pobytu()
        utility.vypiš_odstavec(místnost.popis())

        if not místnost.navštívena:
            fronta_příkazů.clear()

            místnost.navštívena = True
            if hráč.svět.vše_navštíveno():
                utility.uděl_odměnu(hráč, 100, 'prozkoumání všech míst')
            if místnost is hráč.svět.začátek:
                utility.vypiš_odstavec(
                    'Svou rodnou vesnici, stejně jako vcelku poklidný život'
                    ' pekařského učedníka, jsi nechal daleko za sebou a vydal'
                    ' ses na nejistou dráhu dobrodruha.'
                )
                utility.vypiš_odstavec(
                    'Uvnitř pověstmi opředené hory se prý ukrývá pětice'
                    ' posvátných magických předmětů, které i obyčejnému'
                    ' smrtelníkovi mohou přinést nadlidské schopnosti.'
                )

        if místnost is hráč.svět.začátek and hráč.svět.poklad_posbírán():
            utility.zobraz_gratulaci()
            break

        while True:
            místnost.dopad_na_hráče(hráč)

            if not hráč.žije():
                raise SystemExit

            akce = utility.vyber_akci(hráč, fronta_příkazů)
            akce()

            # v případě pohybu vyskočit do vnější smyčky a vypsat popis
            # místnosti
            if akce in (hráč.jdi_na_sever, hráč.jdi_na_jih,
                        hráč.jdi_na_východ, hráč.jdi_na_západ):
                break


if __name__ == '__main__':
    try:
        hra()
    except SystemExit:
        print('\nHra končí.')
