import base64

texty_jeskyně = (
    'Procházíš spletí nepříjemně tísnivých podzemních chodeb.',
    'Našlapuješ po rozměklé zemi ve vlhké a zatuchlé jeskyni.',
    'Jdeš vlhkou a chladnou jeskyní.',
    'Procházíš zapáchajícími jeskynními chodbami.',
    'Jdeš špinavými štolami s těžko dýchatelným vzduchem.',
    'Klopýtáš v téměř dokonalé temnotě této části jeskyně.',
)

texty_les = (
    'Kráčíš zlověstným tichem zšeřelého lesa.',
    'Jdeš po úzké, zarostlé lesní pěšině.',
    'Procházíš nejtmavší a nejponuřejší částí lesa.',
    'Jdeš po sotva znatelné lesní stezce.',
    'Procházíš hustým porostem prastarého lesa.',
)

úvodní_text = (
    'Svou rodnou vesnici, stejně jako vcelku poklidný život pekařského'
    ' učedníka, jsi nechal daleko za sebou a vydal ses na nejistou dráhu'
    ' dobrodruha.',
    'Uvnitř pověstmi opředené hory se prý ukrývá pětice posvátných magických'
    ' předmětů, které i obyčejnému smrtelníkovi mohou přinést nadlidské'
    ' schopnosti.',
)

data_zbraní = (
    ('Cizokrajná šavle', 18, 76, 'Cizokrajnou šavli'),
    ('Ostnatý palcát', 17, 64),
    ('Zkrvavená mačeta', 16, 54, 'Zkrvavenou mačetu'),
)

data_léků = (
    ('Léčivé bylinky', 16, 18, 'Léčivými bylinkami'),
    ('Léčivé bylinky', 17, 19, 'Léčivými bylinkami'),
    ('Kouzelné bylinky', 21, 22, 'Kouzelnými bylinkami'),
    ('Kouzelné bylinky', 22, 23, 'Kouzelnými bylinkami'),
    ('Léčivé houby', 13, 12, 'Léčivými houbami'),
    ('Kouzelné houby', 20, 24, 'Kouzelnými houbami'),
    ('Kouzelné houby', 21, 25, 'Kouzelnými houbami'),
    ('Léčivé bobule', 13, 10, 'Léčivými bobulemi'),
    ('Kouzelné bobule', 17, 17, 'Kouzelnými bobulemi'),
    ('Kouzelné bobule', 18, 18, 'Kouzelnými bobulemi'),
    ('Plástev lesního medu', 12, 11, 'Pláství lesního medu'),
    ('Plástev lesního medu', 13, 12, 'Pláství lesního medu'),
    ('Hadí ocásek', 14, 16, 'Hadím ocáskem'),
    ('Ještěrčí ocásek', 15, 20, 'Ještěrčím ocáskem'),
)

data_artefaktů = (
    ('Křišťálová koule', None, 'Křišťálovou kouli'),
    ('Rubínový kříž', 'červená'),
    ('Tyrkysová tiára', 'tyrkys', 'Tyrkysovou tiáru'),
    ('Ametystový kalich', 'fialová'),
    ('Safírový trojzubec', 'modrá'),
)

mapa_b64 = (
    'Zm0gICAgICAgIGdjIGNjY2MgQSAgICAgICAgICAgICAgICAgICAgICAKIGZmZiAgICBsYy'
    'BDIGMgIENjYyAgICAgICAgICAgICAgICAgICAgICAKICBmICAgICAgY2NjY2NjICAgIGMg'
    'ICAgICAgICBnYyAgICAgICAgICAKICBGICBmICAgICAgICBjSGNjIGMgYyAgY2cgICAgQy'
    'BsYyAgICAgICAKIGZmIGZGZiAgIGNjQyBjICBjY2NjY2MgYyAgICBjYyAgY2NjZyAgICAK'
    'IGYgIGYgZiAgIGMgY2NjICBjICAgVCAgYyAgY1RjIGNjQyAgICAgICAKIGZmIGYgbSBmIE'
    'EgICBjICBjdyBjY2NjY2NjYyBjY2MgYyAgICAgICAKZiBmZmYgZmZmICAgYyAgICAgICAg'
    'ICBDICBDICAgICAgY0EgICAgICAKZiBGIG0gICBmVyAgYyAgY2djYyBjIGNjY2NjY2MgIC'
    'AgICAgICAgICAKZm1mICAgICAgY2NjYyAgYyAgYyBjY2MgICAgICAgYyAgZyBjICAgICAK'
    'ZiBmZiAgICBjICAgY0NjYyBjQ2NjIEMgZyAgIGNjYyAgYyBjbCAgICAKZmYgZiAgIENjY2'
    'NjYyAgY2NjICBjIGMgYyBjY2MgIGMgY2NjICAgICAKIEYgbSAgY2MgIGMgY2dDYyBjIHdj'
    'IGNjY0NjIGNUY2NjYyAgICAgICAKbWYgICAgZyAgY2MgYyAgICAgICBjIGMgIGMgICAgYy'
    'AgY0NjICAgICAKIGZmICAgY2MgYyAgICAgICAgZiAgIGcgY2MgICAgZ2MgICB3ICAgICAK'
    'ICAgICAgICAgVCAgICBGZm0gZiAgICAgYyAgICAgICAgICAgICAgICAKICAgICAgICAgY2'
    'cgICBmICBmZmZmICAgTSAgICAgICAgICAgICAgICAKICAgICAgICAgYyBjICBmZmZmIHQg'
    'ICAgZiAgICAgICAgICAgZmYgZiAKICAgICAgIGNjQ2NjICAgeCAgIGYgbWYgZiBmZmZmIG'
    '0gICAgIGZmRmYKICAgY2MgY2MgIGMgICAgICAgbWYgIGZmZiAgZiBmZmYgIGZmIGYgIG0K'
    'ICAgIGMgIGMgY2NDYyBsYyAgIGZmZiAgZkZmZiAgIEYgICBmRmZmICAKICAgIGNjY2MgYy'
    'AgYyAgY0EgICAgRiAgZiAgbSBmZmYgZmZmICBmZiAKICAgQ2MgZyAgYyBjY2MgQyAgICAg'
    'ZmZmZmYgICBmICAgZiAgZiBmICAKICAgYyAgYyAgYyB3IGNjYyAgICAgbSBmIGYgeGZmRm'
    'YgZm0gZmZGZmYKICAgY0EgICAgICAgICAgICAgICAgICBmIGYgIGYgIGZmZiAgZiAgIGYK'
    'ICAgICAgICAgICAgICAgICAgICAgICAgICAgIGZmbSAgZiBmbSBmZmYKICAgICAgICAgIC'
    'AgICAgICAgICAgICAgICAgICAgICAgZiBmIGZmIGYKICAgICAgICAgICAgICAgICAgICAg'
    'ICAgICAgICAgICAgUyAgICAgbWY='
)

mapa = base64.b64decode(mapa_b64.encode()).decode()

if mapa.count('1') > len(data_artefaktů):
    raise ValueError('Nedostatek dat pro artefakty')
if mapa.count('S') != 1:
    raise ValueError('Na mapě musí být přesně jedna startovní místnost')

řádky_mapy = mapa.split('\n')

počáteční_inventář = (
    (
        'Zbraň',
        ('Tupý nůž', 5, 13),
    ),
    (
        'Lék',
        ('Bylinkový chleba', 8, 10, 'Bylinkovým chlebem'),
    ),
)
