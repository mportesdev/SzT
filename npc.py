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
        self.text = ('Na zemi sedí vousatý hromotluk. V plátěném'
                     ' pytli má nějaké věci, určené patrně na prodej.')
        self.gold = 200
        self.inventory = [
            items.Consumable('Léčivý lektvar', 40, 48),
            items.Consumable('Hojivá mast', 11, 12, 'Hojivou mast'),
            items.Consumable('Hojivá mast', 14, 16, 'Hojivou mast'),
            items.Consumable('Léčivý lektvar', 45, 54),
            items.Consumable('Bylinkový chleba', 10, 7),
        ]
        self.slang = ('prašule', 'vašnosto')
