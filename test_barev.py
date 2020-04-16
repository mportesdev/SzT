from szt.utility import vypiš_barevně
from szt.veci import Zbraň, Lék


def main():
    vypiš_barevně('[červená]červená[/][modrá]modrá[/]'
                  '[fialová]fialová[/][tyrkys]tyrkys')

    vypiš_barevně('[modrá]Číslo položky             ([/]'
                  'Enter[modrá] = návrat)')

    vypiš_barevně('K[modrá]: koupit    [/]P[modrá]: prodat    ([/]'
                  'Enter[modrá] = návrat)')

    vypiš_barevně('[', barva='modrá', end='')
    vypiš_barevně(' + [modrá]les[/]           # '
                  '[modrá]jeskyně[/]         H [modrá]hráč[/]'
                  '            ? [modrá]neznámo ]')

    vypiš_barevně('[ Zdraví:', barva='fialová', end='')
    vypiš_barevně(f' {64:3} {"%":<4}'
                  f'[fialová]zkušenost:[/] {1024:<7}'
                  f'[fialová]zlato:[/] 128 [fialová]]')

    vypiš_barevně('[modrá]Opravdu skončit? ([/]A [modrá]/[/] N[modrá])')

    zbraň = Zbraň('Halapartna', 19, 99, 'Halapartnu')
    vypiš_barevně(zbraň)

    lék = Lék('Lahvička lektvaru', 27, 37, 'Lahvičkou lektvaru',
              'Lahvičku lektvaru')
    vypiš_barevně(lék)


if __name__ == '__main__':
    main()
