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
        self.inventory = [items.Consumable('Bochník chleba', 3, 2),
                          items.Consumable('Bochník chleba', 3, 2),
                          items.Consumable('Hojivá mast', 12, 12),
                          items.Consumable('Hojivá mast', 12, 12),
                          items.Consumable('Léčivý lektvar', 50, 60),
                          items.Consumable('Léčivý lektvar', 50, 60)]
