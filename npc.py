# coding: utf-8

import items


class Obchodník:
    def __init__(self, jméno, text, zlato, inventář, mluva):
        self.jméno = jméno
        self.text = text
        self.zlato = zlato
        self.inventář = inventář
        self.mluva = mluva
        self.marže = 10

    def __str__(self):
        return self.jméno

    def výkupní_cena(self, věc):
        return věc.cena * (100 - self.marže) // 100

    @classmethod
    def mastičkář(cls):
        return cls(jméno='Mastičkář',
                   text=('Na zemi sedí vousatý hromotluk. V plátěném pytli má'
                         ' nějaké věci, určené patrně na prodej.'),
                   zlato=350,
                   inventář=[
                       items.Léčivka('Hojivá mast', 11, 13, 'Hojivou mastí',
                                        'Hojivou mast'),
                       items.Léčivka('Lahvička medicíny', 28, 37,
                                        'Lahvičkou medicíny',
                                        'Lahvičku medicíny'),
                       items.Léčivka('Léčivý lektvar', 39, 53,
                                        'Léčivým lektvarem'),
                       items.Zbraň('Zálesácká sekerka', 12, 51,
                                    'Zálesáckou sekerku'),
                       items.Léčivka('Speciální lektvar', 52, 67,
                                        'Speciálním lektvarem'),
                             ],
                   mluva=('prašule', 'vašnosto'))

    @classmethod
    def zbrojíř(cls):
        return cls(jméno='Zbrojíř',
                   text=('Ve stínu stojí prošedivělý sporý chlápek v kožené'
                         ' vestě a bronzové přilbici.'),
                   zlato=450,
                   inventář=[
                       items.Zbraň('Obouruční meč', 24, 112),
                       items.Zbraň('Těžká sekera', 26, 121, 'Těžkou sekeru'),
                       items.Léčivka('Hojivá mast', 14, 18, 'Hojivou mastí',
                                        'Hojivou mast'),
                       items.Zbraň('Halapartna', 19, 99, 'Halapartnu'),
                             ],
                   mluva=('finance', 'sire'))
