# coding: utf-8

import random

import items


class Enemy:
    def __init__(self, name, hp, damage,
                 name_dative=None, name_accusative=None,
                 alive_text=None, dead_text=None):
        self.name = name
        self.name_short = self.name.split()[-1].lower()
        self.hp = hp
        self.damage = damage

        self.name_dative = name_dative or self.name
        self.name_accusative = name_accusative or self.name

        self.alive_text = alive_text or f'Zaútočil na tebe {self.name.lower()}!'
        self.dead_text = dead_text or f'Na zemi leží mrtvý {self.name.lower()}.'

    def __str__(self):
        return self.name

    def is_alive(self):
        return self.hp > 0

    @property
    def text(self):
        return self.alive_text if self.is_alive() else self.dead_text


class Animal(Enemy):
    """Enemies of this class only cause damage to the player and take
    damage from the player's attacks.
    """
    pass


class Monster(Enemy):
    """Enemies of this class cause damage to the player, take damage
    from the player's attacks, and leave a random gold treasure after
    being killed.
    """
    def __init__(self, name, hp, damage,
                 name_dative=None, name_accusative=None,
                 alive_text=None, dead_text=None):
        super().__init__(name, hp, damage,
                         name_dative, name_accusative, alive_text, dead_text)
        self.gold = random.randint(5, 20)
        self.gold_claimed = False

    @classmethod
    def new_troll(cls):
        return cls(name='Kamenný troll',
                   hp=82,
                   damage=14,
                   name_dative='Trollovi',
                   name_accusative='Trolla',
                   alive_text='Vyrušil jsi dřímajícího kamenného trolla!',
                   dead_text='Zabitý kamenný troll připomíná obyčejnou skálu.')


class Human(Enemy):
    """Enemies of this class cause damage to the player, take damage
    from the player's attacks, and drop their weapon after being
    killed, along with an optional amount of gold.
    """
    def __init__(self, name, hp, weapon,
                 name_dative=None, name_accusative=None,
                 alive_text=None, dead_text=None):
        super().__init__(name, hp, None,
                         name_dative, name_accusative, alive_text, dead_text)
        self.weapon = weapon
        self.weapon_claimed = False
        self.damage = self.weapon.damage
        self.gold = random.choice((0, random.randint(5, 15)))
        self.gold_claimed = False

    @classmethod
    def new_human(cls):
        return cls(name='Cizí dobrodruh',
                   hp=80,
                   weapon=items.Weapon('Železné kopí', 18, 85),
                   name_dative='Dobrodruhovi',
                   name_accusative='Dobrodruha',
                   alive_text='Vrhl se na tebe pološílený dobrodruh - jiný hráč'
                              ' této hry!',
                   dead_text='Na zemi leží mrtvola muže s vytřeštěnýma očima.')


enemies_data = (
    (
        Animal,
        {
            'name': 'Obří pavouk',
            'hp': 24,
            'damage': 6,
            'name_dative': 'Pavoukovi',
            'name_accusative': 'Pavouka',
            'alive_text': 'Z výšky se spustil obří pavouk a snaží se tě'
                          ' pozřít!',
            'dead_text': 'Na zemi se válí kusy gigantického pavouka.',
        },
    ),

    (
        Animal,
        {
            'name': 'Obří šváb',
            'hp': 28,
            'damage': 4,
            'name_dative': 'Švábovi',
            'name_accusative': 'Švába',
            'alive_text': 'Z díry vylezl odporný obří šváb a sevřel tě'
                          ' kusadly!',
            'dead_text': 'Na zemi leží tlející mrtvola švába.',
        },
    ),

    (
        Monster,
        {
            'name': 'Skřet',
            'hp': 42,
            'damage': 10,
            'name_dative': 'Skřetovi',
            'name_accusative': 'Skřeta',
        },
    ),

    (
        Monster,
        {
            'name': 'Krysodlak',
            'hp': 45,
            'damage': 12,
            'name_dative': 'Krysodlakovi',
            'name_accusative': 'Krysodlaka',
        },
    ),

    (
        Animal,
        {
            'name': 'Jeskynní dráček',
            'hp': 55,
            'damage': 8,
            'name_dative': 'Dráčkovi',
            'name_accusative': 'Dráčka',
            'alive_text': 'Ze tmy vyskočil malý jeskynní dráček a zasáhl tě'
                          ' ohnivou koulí!',
            'dead_text': 'Z mrtvoly jeskynního dráčka vytéká jasně oranžová'
                         ' tekutina.',
        },
    ),
)


def random_enemy():
    enemy_class, kwargs = random.choice(enemies_data)
    return enemy_class(**kwargs)
