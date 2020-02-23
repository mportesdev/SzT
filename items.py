# coding: utf-8


class Věc:
    def __init__(self, název, cena, název_4_pád=None):
        self.název = název
        self.cena = cena
        self.název_4_pád = název_4_pád or self.název

    def __str__(self):
        return self.název_4_pád


class Zbraň(Věc):
    def __init__(self, název, útok, cena, název_4_pád=None):
        super().__init__(název, cena, název_4_pád)
        self.útok = útok

    def __str__(self):
        return f'{self.název_4_pád} (útok +{self.útok})'


class Léčivka(Věc):
    def __init__(self, název, léčivá_síla, cena, název_7_pád, název_4_pád=None):
        super().__init__(název, cena, název_4_pád)
        self.léčivá_síla = léčivá_síla
        self.název_7_pád = název_7_pád

    def __str__(self):
        return f'{self.název_4_pád} (zdraví +{self.léčivá_síla})'

    def str_7(self):
        return f'{self.název_7_pád} (zdraví +{self.léčivá_síla})'


class Artefakt(Věc):
    def __init__(self, název, barva, název_4_pád=None):
        super().__init__(název, None, název_4_pád)
        self.barva = barva
