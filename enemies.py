# coding: utf-8

import random

import items


class Enemy:
    def __init__(self):
        raise NotImplementedError('Do not create raw Enemy objects.')

    def __str__(self):
        return self.name

    def is_alive(self):
        return self.hp > 0


class Animal(Enemy):
    """Simple and easy to defeat enemy class.

    Objects of this class only cause damage to the player and take
    damage from the player's attacks.
    """
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
    """Slightly tougher enemy class.

    Objects of this class cause damage to the player, take damage from
    the player's attacks, and leave a random gold treasure after being
    killed.
    """
    def __init__(self, name, hp, damage,
                 name_dative=None, name_accusative=None,
                 alive_text=None, dead_text=None):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.gold = random.randint(5, 20)
        self.gold_claimed = False

        self.name_dative = name_dative or self.name
        self.name_accusative = name_accusative or self.name

        self.alive_text = alive_text or f'Zaútočil na tebe {self.name.lower()}.'
        self.dead_text = dead_text or f'Leží tu mrtvý {self.name.lower()}.'

    @property
    def text(self):
        return self.alive_text if self.is_alive() else self.dead_text


class Human(Enemy):
    """Tough enemy class.

    Objects of this class cause damage to the player, take damage from
    the player's attacks, and drop their weapon after being killed,
    along with an optional amount of gold.
    """
    def __init__(self, name, hp,
                 name_dative=None, name_accusative=None,
                 alive_text=None, dead_text=None):
        self.name = name
        self.hp = hp
        self.weapon = items.ColdWeapon('Rezavý meč', 20, 100)
        self.weapon_claimed = False
        self.damage = self.weapon.damage
        self.gold = random.randint(0, 10)
        self.gold_claimed = False

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

    (
        Human,
        {
            'name': 'Cizí dobrodruh',
            'hp': 100,
            'name_dative': 'Dobrodruhovi',
            'name_accusative': 'Dobrodruha',
            'alive_text': 'Vrhl se na tebe pološílený dobrodruh - jiný hráč'
                          ' této hry!',
            'dead_text': 'Na zemi leží mrtvola muže s vytřeštěnýma očima.',
        },
    ),
)
