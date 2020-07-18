# coding: utf-8


class Věc:
    def __init__(já, název, cena, název_4_pád=None):
        já.název = název
        já.cena = cena
        já.název_4_pád = název_4_pád or já.název


class Zbraň(Věc):
    def __init__(já, název, útok, cena, název_4_pád=None, název_ve_větě=None):
        super().__init__(název, cena, název_4_pád)
        já.útok = útok
        já.název_ve_větě = název_ve_větě or já.název_4_pád.lower()

    def __format__(já, format_spec):
        if format_spec == '4':
            return f'{já.název_4_pád} ([fialová]útok +{já.útok}[/])'

        return super().__format__(format_spec)


class Lék(Věc):
    def __init__(já, název, léčivá_síla, cena, název_7_pád, název_4_pád=None,
                 speciální=False):
        super().__init__(název, cena, název_4_pád)
        já.léčivá_síla = léčivá_síla
        já.název_7_pád = název_7_pád
        já.speciální = speciální

    def __format__(já, format_spec):
        if format_spec == '4':
            return f'{já.název_4_pád} ([tyrkys]zdraví +{já.léčivá_síla}[/])'
        if format_spec == '7':
            return f'{já.název_7_pád} ([tyrkys]zdraví +{já.léčivá_síla}[/])'

        return super().__format__(format_spec)


class Artefakt(Věc):
    def __init__(já, název, barva, název_4_pád=None):
        super().__init__(název, None, název_4_pád)
        já.barva = barva

    def __format__(já, format_spec):
        if format_spec == '4':
            return f'[{já.barva}]< {já.název_4_pád} >[/]'

        return super().__format__(format_spec)
