from . import barvy


def vstup_z_možností(možnosti):
    while True:
        vstup = input()
        for možnost in možnosti:
            if vstup.upper() == str(možnost).upper():
                return možnost
        else:
            barvy.vypiš_barevně('?', barva='fialová')


def vstup_číslo_položky(možnosti):
    barvy.vypiš_barevně(
        '[modrá]Číslo položky             ([/]Enter[modrá] = návrat)',
        end=' '
    )
    return vstup_z_možností(možnosti)


def vstup_koupit_prodat():
    barvy.vypiš_barevně(
        'K[modrá]: koupit    [/]P[modrá]: prodat    ([/]'
        'Enter[modrá] = návrat)',
        end=' '
    )
    return vstup_z_možností({'K', 'P', ''})


def potvrď_konec():
    barvy.vypiš_barevně(
        '[modrá]Opravdu skončit? ([/]A [modrá]/[/] N[modrá])',
        end=' '
    )
    if vstup_z_možností({'A', 'N'}) == 'A':
        raise SystemExit
