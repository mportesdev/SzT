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
                 name_dative=None, name_accusative=None,
                 alive_text=None, dead_text=None):
        self.name = name
        self.hp = hp
        self.damage = damage

        self.name_dative = name_dative or self.name
        self.name_accusative = name_accusative or self.name

        self.alive_text = alive_text or f'Zaútočil na tebe {self.name.lower()}.'
        self.dead_text = dead_text or f'Leží tu mrtvý {self.name.lower()}.'

    @property
    def text(self):
        return self.alive_text if self.is_alive() else self.dead_text


class Monster(Enemy):
    def __init__(self, name, hp, damage,
                 name_dative=None, name_accusative=None,
                 alive_text=None, dead_text=None):
        self.name = name
        self.hp = hp
        self.damage = damage

        self.name_dative = name_dative or self.name
        self.name_accusative = name_accusative or self.name

        self.alive_text = alive_text or f'Zaútočil na tebe {self.name.lower()}.'
        self.dead_text = dead_text or f'Leží tu mrtvý {self.name.lower()}.'

    @property
    def text(self):
        return self.alive_text if self.is_alive() else self.dead_text


enemies_data = (
    (
        Animal,
        {
            'name': 'Obří pavouk',
            'hp': 12,
            'damage': 6,
            'name_dative': 'Pavoukovi',
            'name_accusative': 'Pavouka',
            'alive_text': 'Obří pavouk seskočil ze své sítě přímo před tebe!',
            'dead_text': 'Na zemi leží tlející mrtvola pavouka.',
        },
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
    ),

    (
        Animal,
        {
            'name': 'Kolonie netopýrů',
            'hp': 98,
            'damage': 4,
            'name_dative': 'Netopýrům',
            'name_accusative': 'Netopýry',
            'alive_text': 'Slyšíš postupně sílící pištivý zvuk... náhle jsi'
                          ' uprostřed hejna netopýrů!',
            'dead_text': 'Kolem se povalují desítky mrtvých netopýrů.',
        },
    ),

    (
        Monster,
        {
            'name': 'Kamenný obr',
            'hp': 82,
            'damage': 16,
            'name_dative': 'Obrovi',
            'name_accusative': 'Obra',
            'alive_text': 'Vyrušil jsi dřímajícího kamenného obra!',
            'dead_text': 'Přemožený obr se proměnil nazpět v obyčejnou skálu.',
        },
    ),
)
