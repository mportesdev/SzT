# coding: utf-8

from typing import List, Union

from . import agent, svet, utility, veci

PoložkyInventáře = List[Union[veci.Zbraň, veci.Lék]]


class Hráč:
    def __init__(já):
        já.inventář: PoložkyInventáře = [
            veci.Zbraň('Tupý nůž', 5, 13),
            veci.Lék('Bylinkový chleba', 8, 10, 'Bylinkovým chlebem'),
        ]
        já.artefakty = []
        já.svět = svet.Svět()
        já.x, já.y = já.svět.začátek.x, já.svět.začátek.y
        já.zdraví = 100
        já.zlato = 0
        já.zkušenost = 0
        já.zdařilý_zásah = False
        já.mapování = False

    def žije(já):
        return já.zdraví > 0

    def vypiš_inventář(já):
        agent.vypiš_inventář(já)

    def nejlepší_zbraň(já):
        try:
            return max((věc for věc in já.inventář
                        if hasattr(věc, 'útok')),
                       key=lambda zbraň: zbraň.útok)
        except ValueError:
            return

    def jdi(já, rozdíl_x, rozdíl_y):
        já.x += rozdíl_x
        já.y += rozdíl_y

    def jdi_na_sever(já):
        já.jdi(rozdíl_x=0, rozdíl_y=-1)

    def jdi_na_jih(já):
        já.jdi(rozdíl_x=0, rozdíl_y=1)

    def jdi_na_východ(já):
        já.jdi(rozdíl_x=1, rozdíl_y=0)

    def jdi_na_západ(já):
        já.jdi(rozdíl_x=-1, rozdíl_y=0)

    def bojuj(já):
        nepřítel = já.místnost_pobytu().nepřítel
        zbraň = já.nejlepší_zbraň()
        síla_zbraně = zbraň.útok if zbraň else 1
        skutečný_zásah_zbraní = utility.s_odchylkou(síla_zbraně)
        já.zdařilý_zásah = (skutečný_zásah_zbraní > síla_zbraně * 1.1
                            and nepřítel.krátké_jméno not in ('troll',
                                                              'dobrodruh'))
        útočný_bonus = min(já.zkušenost // 200, 5)
        skutečný_zásah = min(skutečný_zásah_zbraní + útočný_bonus,
                             nepřítel.zdraví)
        nepřítel.zdraví -= skutečný_zásah
        já.zkušenost += skutečný_zásah
        agent.zpráva_o_útoku(zbraň, nepřítel)
        if já.svět.nepřátelé_pobiti():
            agent.uděl_odměnu(já, 200, 'zabití všech nepřátel')

    def má_léky(já):
        return any(isinstance(věc, veci.Lék) for věc in já.inventář)

    def kurýruj_se(já):
        léky = [věc for věc in já.inventář if isinstance(věc, veci.Lék)]

        lék = agent.dialog_léčení(léky)
        if lék:
            já.spotřebuj(lék)

    def spotřebuj(já, lék):
        if lék.speciální:
            já.zdraví += lék.léčivá_síla
        else:
            já.zdraví += min(lék.léčivá_síla, 100 - já.zdraví)
        já.inventář.remove(lék)

    def obchoduj(já):
        já.místnost_pobytu().obchoduj(já)

    def kup(já, věc, prodejce):
        prodejce.inventář.remove(věc)
        já.inventář.append(věc)
        cena = věc.cena
        prodejce.zlato += cena
        já.zlato -= cena

    def prodej(já, věc, kupující):
        já.inventář.remove(věc)
        kupující.inventář.append(věc)
        cena = kupující.výkupní_cena(věc)
        já.zlato += cena
        kupující.zlato -= cena

    def místnost_pobytu(já):
        return já.svět[já.x, já.y]

    def nakresli_mapu(já):
        agent.nakresli_mapu(já.svět, (já.x, já.y))
