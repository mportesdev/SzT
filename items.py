# coding: utf-8


class Weapon:
    def __init__(self):
        raise NotImplementedError('Do not create raw Weapon objects.')

    def __str__(self):
        return self.name


class ColdWeapon(Weapon):
    def __init__(self, name, damage, value, name_accusative=None):
        self.name = name
        self.damage = damage
        self.value = value
        self.name_accusative = name_accusative or self.name


class Consumable:
    def __init__(self):
        raise NotImplementedError('Do not create raw Consumable objects.')

    def __str__(self):
        return f'{self.name} (+{self.healing_value} % zdraví)'


class Bread(Consumable):
    def __init__(self):
        self.name = 'Bochník chleba'
        self.healing_value = 3
        self.value = 2


class Salve(Consumable):
    def __init__(self):
        self.name = 'Hojivá mast'
        self.healing_value = 12
        self.value = 12


class HealingPotion(Consumable):
    def __init__(self):
        self.name = 'Léčivý lektvar'
        self.healing_value = 50
        self.value = 60
