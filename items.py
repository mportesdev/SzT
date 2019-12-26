# coding: utf-8


class Weapon:
    def __init__(self):
        raise NotImplementedError('Do not create raw Weapon objects.')

    def __str__(self):
        return self.name


class Rock(Weapon):
    def __init__(self):
        self.name = 'Kámen'
        self.damage = 5
        self.value = 1


class Dagger(Weapon):
    def __init__(self):
        self.name = 'Dýku'
        self.damage = 10
        self.value = 20


class RustySword(Weapon):
    def __init__(self):
        self.name = 'Rezavý meč'
        self.damage = 20
        self.value = 100


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
