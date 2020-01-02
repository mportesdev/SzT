# coding: utf-8

import items


class NonPlayableCharacter:
    def __init__(self):
        raise NotImplementedError('Do not create raw NPC objects.')

    def __str__(self):
        return self.name


class Trader(NonPlayableCharacter):
    def __init__(self):
        self.name = 'Obchodník'
        self.gold = 200
        self.inventory = [items.Bread(),
                          items.Bread(),
                          items.Salve(),
                          items.Salve(),
                          items.HealingPotion(),
                          items.HealingPotion()]
