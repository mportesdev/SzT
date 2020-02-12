# coding: utf-8


class Item:
    def __init__(self, name, value, name_4=None):
        self.name = name
        self.value = value
        self.name_4 = name_4 or self.name

    def __str__(self):
        return self.name_4


class Weapon(Item):
    def __init__(self, name, damage, value, name_4=None):
        super().__init__(name, value, name_4)
        self.damage = damage

    def __str__(self):
        return f'{self.name_4} (útok +{self.damage})'


class Consumable(Item):
    def __init__(self, name, healing_value, value, name_7, name_4=None):
        super().__init__(name, value, name_4)
        self.healing_value = healing_value
        self.name_7 = name_7

    def __str__(self):
        return f'{self.name_4} (zdraví +{self.healing_value})'

    def str_7(self):
        return f'{self.name_7} (zdraví +{self.healing_value})'


class Artifact(Item):
    def __init__(self, name, color, name_4=None):
        super().__init__(name, None, name_4)
        self.color = color
