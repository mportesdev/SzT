# coding: utf-8


class Weapon:
    def __init__(self, name, damage, value, name_accusative=None):
        self.name = name
        self.damage = damage
        self.value = value
        self.name_accusative = name_accusative or self.name

    def __str__(self):
        return f'{self.name_accusative} (útok +{self.damage})'


class Consumable:
    def __init__(self, name, healing_value, value, name_accusative=None):
        self.name = name
        self.healing_value = healing_value
        self.value = value
        self.name_accusative = name_accusative or self.name

    def __str__(self):
        return f'{self.name_accusative} (+{self.healing_value} % zdraví)'
