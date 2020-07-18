# coding: utf-8


class Věc:
    def __init__(self, název, cena, název_4_pád=None):
        self.název = název
        self.cena = cena
        self.název_4_pád = název_4_pád or self.název


class Zbraň(Věc):
    def __init__(self, název, útok, cena, název_4_pád=None, název_ve_větě=None):
        super().__init__(název, cena, název_4_pád)
        self.útok = útok
        self.název_ve_větě = název_ve_větě or self.název_4_pád.lower()

    def __format__(self, format_spec):
        if format_spec == '4':
            return f'{self.název_4_pád} ([fialová]útok +{self.útok}[/])'

        return super().__format__(format_spec)


class Lék(Věc):
    def __init__(self, název, léčivá_síla, cena, název_7_pád, název_4_pád=None,
                 speciální=False):
        super().__init__(název, cena, název_4_pád)
        self.léčivá_síla = léčivá_síla
        self.název_7_pád = název_7_pád
        self.speciální = speciální

    def __format__(self, format_spec):
        if format_spec == '4':
            return f'{self.název_4_pád} ([tyrkys]zdraví +{self.léčivá_síla}[/])'
        if format_spec == '7':
            return f'{self.název_7_pád} ([tyrkys]zdraví +{self.léčivá_síla}[/])'

        return super().__format__(format_spec)


class Artefakt(Věc):
    def __init__(self, název, barva, název_4_pád=None):
        super().__init__(název, None, název_4_pád)
        self.barva = barva

    def __format__(self, format_spec):
        if format_spec == '4':
            return f'[{self.barva}]< {self.název_4_pád} >[/]'

        return super().__format__(format_spec)
