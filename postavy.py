# coding: utf-8

import veci


class Obchodník:
    def __init__(já, jméno, text, zlato, inventář, mluva):
        já.jméno = jméno
        já.text = text
        já.zlato = zlato
        já.inventář = inventář
        já.mluva = mluva
        já.marže = 10

    def __str__(já):
        return já.jméno

    def výkupní_cena(já, věc):
        return věc.cena * (100 - já.marže) // 100

    @classmethod
    def mastičkář(třída):
        return třída(jméno='Mastičkář',
                     text=('Na zemi sedí vousatý hromotluk. V plátěném pytli má'
                           ' nějaké věci, určené patrně na prodej.'),
                     zlato=350,
                     inventář=[
                         veci.Lék('Léčivý přípravek', 39, 53,
                                  'Léčivým přípravkem'),
                         veci.Lék('Hojivá mast', 14, 18, 'Hojivou mastí',
                                  'Hojivou mast'),
                         veci.Zbraň('Zálesácká sekerka', 12, 51,
                                    'Zálesáckou sekerku'),
                         veci.Lék('Speciální životabudič', 52, 67,
                                  'Speciálním životabudičem'),
                         veci.Lék('Elixír života', 90, 256,
                                  'Elixírem života'),
                               ],
                     mluva=('prašule', 'vašnosto'))

    @classmethod
    def zbrojíř(třída):
        return třída(jméno='Zbrojíř',
                     text=('Ve stínu stojí prošedivělý sporý chlápek v kožené'
                           ' vestě a bronzové přilbici.'),
                     zlato=450,
                     inventář=[
                         veci.Zbraň('Válečnický meč', 24, 114),
                         veci.Zbraň('Řemdih Smrtonoš', 32, 256),
                         veci.Lék('Lahvička lektvaru', 28, 37,
                                  'Lahvičkou lektvaru',
                                  'Lahvičku lektvaru'),
                         veci.Zbraň('Halapartna', 19, 99, 'Halapartnu'),
                         veci.Lék('Léčivá mast', 11, 13, 'Léčivou mastí',
                                  'Léčivou mast'),
                               ],
                     mluva=('finance', 'sire'))
