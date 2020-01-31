# coding: utf-8

import random

import items


class Enemy:
    def __init__(self, name, hp, damage,
                 name_3=None, name_4=None,
                 alive_text=None, dead_text=None):
        self.name = name
        self.name_short = self.name.split()[-1].lower()
        self.hp = hp
        self.damage = damage

        self.name_3 = name_3 or self.name
        self.name_4 = name_4 or self.name

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
                 name_3=None, name_4=None,
                 alive_text=None, dead_text=None):
        super().__init__(name, hp, damage,
                         name_3, name_4, alive_text, dead_text)
        self.gold = random.randint(8, 16)
        self.gold_claimed = False

    @classmethod
    def new_troll(cls):
        return cls(name='Kamenný troll',
                   hp=92,
                   damage=16,
                   name_3='Trollovi',
                   name_4='Trolla',
                   alive_text='Vyrušil jsi dřímajícího kamenného trolla!',
                   dead_text='Zabitý kamenný troll připomíná obyčejnou skálu.')

    @classmethod
    def new_forest_troll(cls):
        return cls(name='Lesní troll',
                   hp=62,
                   damage=12,
                   name_3='Trollovi',
                   name_4='Trolla',
                   alive_text='Cestu ti zastoupil mohutný troll obrostlý'
                              ' mechem.')


class Human(Enemy):
    """Enemies of this class cause damage to the player, take damage
    from the player's attacks, and drop their weapon after being
    killed, along with an optional amount of gold.
    """
    def __init__(self, name, hp, weapon,
                 name_3=None, name_4=None,
                 alive_text=None, dead_text=None):
        super().__init__(name, hp, None,
                         name_3, name_4, alive_text, dead_text)
        self.weapon = weapon
        self.weapon_claimed = False
        self.damage = self.weapon.damage
        self.gold = random.choice((0, random.randint(10, 20)))
        self.gold_claimed = False

    @classmethod
    def new_human(cls):
        return cls(name='Cizí dobrodruh',
                   hp=98,
                   weapon=items.Weapon('Železné kopí', 18, 85),
                   name_3='Dobrodruhovi',
                   name_4='Dobrodruha',
                   alive_text='Vrhl se na tebe pološílený dobrodruh - jiný hráč'
                              ' této hry!',
                   dead_text='Na zemi leží mrtvola muže s vytřeštěnýma očima.')


enemies_data = (
    (
        Animal,
        {
            'name': 'Obří pavouk',
            'hp': 29,
            'damage': 7,
            'name_3': 'Pavoukovi',
            'name_4': 'Pavouka',
            'alive_text': 'Z výšky se spustil obří pavouk a snaží se tě'
                          ' pozřít!',
            'dead_text': 'Na zemi se povalují nohy a trup gigantického'
                         ' pavouka.',
        },
    ),

    (
        Animal,
        {
            'name': 'Obří šváb',
            'hp': 33,
            'damage': 5,
            'name_3': 'Švábovi',
            'name_4': 'Švába',
            'alive_text': 'Z díry vylezl odporný obří šváb a sevřel tě'
                          ' kusadly!',
            'dead_text': 'Na zemi leží ohavná tlející mrtvola švába.',
        },
    ),

    (
        Animal,
        {
            'name': 'Obří netopýr',
            'hp': 36,
            'damage': 6,
            'name_3': 'Netopýrovi',
            'name_4': 'Netopýra',
            'dead_text': 'Na zemi leží odpudivý mrtvý netopýr s polámanými'
                         ' kožnatými křídly.',
        },
    ),

    (
        Monster,
        {
            'name': 'Skřet',
            'hp': 43,
            'damage': 12,
            'name_3': 'Skřetovi',
            'name_4': 'Skřeta',
        },
    ),

    (
        Monster,
        {
            'name': 'Krysodlak',
            'hp': 47,
            'damage': 10,
            'name_3': 'Krysodlakovi',
            'name_4': 'Krysodlaka',
        },
    ),

    (
        Animal,
        {
            'name': 'Jeskynní dráček',
            'hp': 54,
            'damage': 9,
            'name_3': 'Dráčkovi',
            'name_4': 'Dráčka',
            'alive_text': 'Ze tmy vyskočil malý jeskynní dráček a zasáhl tě'
                          ' ohnivou koulí!',
            'dead_text': 'Z mrtvoly jeskynního dráčka vytéká jasně oranžová'
                         ' tekutina.',
        },
    ),

    (
        Animal,
        {
            'name': 'Vlk',
            'hp': 28,
            'damage': 5,
            'name_3': 'Vlkovi',
            'name_4': 'Vlka',
            'alive_text': 'Z křoví na tebe vyskočil vychrtlý šedý vlk.',
        },
    ),

    (
        Monster,
        {
            'name': 'Vlkodlak',
            'hp': 39,
            'damage': 9,
            'name_3': 'Vlkodlakovi',
            'name_4': 'Vlkodlaka',
        },
    ),
)


def random_cave_enemy():
    enemy_class, kwargs = random.choice(enemies_data[:6])
    return enemy_class(**kwargs)


def random_forest_enemy():
    enemy_class, kwargs = random.choice(enemies_data[6:])
    return enemy_class(**kwargs)
