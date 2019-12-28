# coding: utf-8


class Enemy:
    def __init__(self):
        raise NotImplementedError('Do not create raw Enemy objects.')

    def __str__(self):
        return self.name

    def is_alive(self):
        return self.hp > 0


class Animal(Enemy):
    def __init__(self, name, hp, damage,
                 name_dative=None, name_accusative=None):
        self.name = name
        self.hp = hp
        self.damage = damage

        self.name_dative = name_dative or self.name
        self.name_accusative = name_accusative or self.name


class Monster(Enemy):
    def __init__(self, name, hp, damage,
                 name_dative=None, name_accusative=None):
        self.name = name
        self.hp = hp
        self.damage = damage

        self.name_dative = name_dative or self.name
        self.name_accusative = name_accusative or self.name


enemies_data = (
    (
        Animal,
        {
            'name': 'Obří pavouk',
            'hp': 12,
            'damage': 6,
            'name_dative': 'Pavoukovi',
            'name_accusative': 'Pavouka',
        },
        (
            'Obří pavouk seskočil ze své sítě přímo před tebe!',
            'Na zemi leží tlející mrtvola pavouka.',
        ),
    ),

    (
        Monster,
        {
            'name': 'Zlobr',
            'hp': 32,
            'damage': 12,
            'name_dative': 'Zlobrovi',
            'name_accusative': 'Zlobra',
        },
        (
            'Cestu ti zastoupil zlobr!',
            'Zde leží mrtvý zlobr, kterého jsi sám zdolal.',
        ),
    ),

    (
        Animal,
        {
            'name': 'Kolonie netopýrů',
            'hp': 98,
            'damage': 4,
            'name_dative': 'Netopýrům',
            'name_accusative': 'Netopýry',
        },
        (
            'Slyšíš postupně sílící pištivý zvuk... náhle jsi uprostřed hejna'
            ' netopýrů!',
            'Kolem se povalují desítky mrtvých netopýrů.',
        ),
    ),

    (
        Monster,
        {
            'name': 'Kamenný obr',
            'hp': 82,
            'damage': 16,
            'name_dative': 'Obrovi',
            'name_accusative': 'Obra',
        },
        (
            'Vyrušil jsi dřímajícího kamenného obra!',
            'Přemožený obr se proměnil nazpět v obyčejnou skálu.',
        ),
    ),
)
