# coding: utf-8


class Weapon:
    def __init__(self):
        raise NotImplementedError('Do not create raw Weapon objects.')

    def __str__(self):
        return self.name


class ColdWeapon(Weapon):
    def __init__(self, name, damage, value):
        self.name = name
        self.damage = damage
        self.value = value


class Consumable:
    def __init__(self):
        raise NotImplementedError('Do not create raw Consumable objects.')

    def __str__(self):
        return f'{self.name} (+{self.healing_value} % zdraví)'


class CrustyBread(Consumable):
    def __init__(self):
        self.name = 'Křupavý chléb'
        self.healing_value = 10
        self.value = 12


class HealingPotion(Consumable):
    def __init__(self):
        self.name = 'Léčivý lektvar'
        self.healing_value = 50
        self.value = 60
