# coding: utf-8

import items


class Trader:
    def __init__(self, name, text, gold, inventory, slang):
        self.name = name
        self.text = text
        self.gold = gold
        self.inventory = inventory
        self.slang = slang
        self.margin = 10

    def __str__(self):
        return self.name

    def buy_price(self, item):
        return item.value * (100 - self.margin) // 100

    @classmethod
    def new_medicine_trader(cls):
        return cls(name='Mastičkář',
                   text=('Na zemi sedí vousatý hromotluk. V plátěném pytli má'
                         ' nějaké věci, určené patrně na prodej.'),
                   gold=350,
                   inventory=[
                       items.Consumable('Hojivá mast', 11, 12, 'Hojivou mast'),
                       items.Consumable('Lahvička medicíny', 28, 34,
                                        'Lahvičku medicíny'),
                       items.Consumable('Léčivý lektvar', 39, 48),
                       items.Weapon('Dýka', 11, 45, 'Dýku'),
                       items.Consumable('Speciální lektvar', 52, 61),
                             ],
                   slang=('prašule', 'vašnosto'))

    @classmethod
    def new_weapon_trader(cls):
        return cls(name='Zbrojíř',
                   text=('Ve stínu stojí vysoký chlapík v kožené vestě a'
                         ' bronzové přilbici.'),
                   gold=450,
                   inventory=[
                       items.Weapon('Obouruční meč', 24, 102),
                       items.Weapon('Těžká sekera', 26, 110, 'Těžkou sekeru'),
                       items.Consumable('Hojivá mast', 14, 16, 'Hojivou mast'),
                             ],
                   slang=('peníze', 'sire'))
