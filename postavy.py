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
                         veci.Lék('Hojivá mast', 11, 13, 'Hojivou mastí',
                                  'Hojivou mast'),
                         veci.Lék('Lahvička medicíny', 28, 37,
                                  'Lahvičkou medicíny',
                                  'Lahvičku medicíny'),
                         veci.Lék('Léčivý lektvar', 39, 53,
                                  'Léčivým lektvarem'),
                         veci.Zbraň('Zálesácká sekerka', 12, 51,
                                    'Zálesáckou sekerku'),
                         veci.Lék('Speciální lektvar', 52, 67,
                                  'Speciálním lektvarem'),
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
                         veci.Lék('Hojivá mast', 14, 18, 'Hojivou mastí',
                                  'Hojivou mast'),
                         veci.Zbraň('Halapartna', 19, 99, 'Halapartnu'),
                               ],
                     mluva=('finance', 'sire'))
