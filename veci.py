# coding: utf-8


class Věc:
    def __init__(já, název, cena, název_4_pád=None):
        já.název = název
        já.cena = cena
        já.název_4_pád = název_4_pád or já.název

    def __str__(já):
        return já.název_4_pád


class Zbraň(Věc):
    def __init__(já, název, útok, cena, název_4_pád=None):
        super().__init__(název, cena, název_4_pád)
        já.útok = útok

    def __str__(já):
        return f'{já.název_4_pád} (útok +{já.útok})'


class Léčivka(Věc):
    def __init__(já, název, léčivá_síla, cena, název_7_pád, název_4_pád=None):
        super().__init__(název, cena, název_4_pád)
        já.léčivá_síla = léčivá_síla
        já.název_7_pád = název_7_pád

    def __str__(já):
        return f'{já.název_4_pád} (zdraví +{já.léčivá_síla})'

    def popis_7_pád(já):
        return f'{já.název_7_pád} (zdraví +{já.léčivá_síla})'


class Artefakt(Věc):
    def __init__(já, název, barva, název_4_pád=None):
        super().__init__(název, None, název_4_pád)
        já.barva = barva
