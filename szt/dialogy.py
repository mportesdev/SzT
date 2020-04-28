# coding: utf-8

from . import konzole


def vstup_z_možností(možnosti):
    while True:
        vstup = input()
        for možnost in možnosti:
            if vstup.upper() == str(možnost).upper():
                return možnost
        else:
            konzole.nerozumím()


def vstup_číslo_položky(možnosti):
    konzole.vypiš_barevně(
        '[modrá]Číslo položky             ([/]Enter[modrá] = návrat)',
        end=' '
    )
    return vstup_z_možností(možnosti)


def vstup_koupit_prodat():
    konzole.vypiš_barevně(
        'K[modrá]: koupit    [/]P[modrá]: prodat    ([/]'
        'Enter[modrá] = návrat)',
        end=' '
    )
    return vstup_z_možností({'K', 'P', ''})


def potvrď_konec():
    konzole.vypiš_barevně(
        '[modrá]Opravdu skončit? ([/]A [modrá]/[/] N[modrá])',
        end=' '
    )
    if vstup_z_možností({'A', 'N'}) == 'A':
        raise SystemExit


def dialog_léčení(léky):
    konzole.vypiš_barevně('Čím se chceš kurýrovat?')
    for číslo, věc in enumerate(léky, 1):
        konzole.vypiš_věc_k_léčení(číslo, věc)

    možnosti = set(range(1, len(léky) + 1))
    vstup = vstup_číslo_položky(možnosti | {''})
    if vstup == '':
        return

    lék = léky[vstup - 1]
    if lék.speciální:
        konzole.vypiš_barevně('Obsah nevelké lahvičky s tebou pořádně zamával.')
    else:
        konzole.vypiš_barevně('Hned se cítíš líp.')

    return lék
