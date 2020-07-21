# coding: utf-8

from . import agent, data, svet, veci, vypocty


class Hráč:
    def __init__(self):
        self.inventář = [getattr(veci, název_třídy)(*parametry)
                       for název_třídy, parametry in data.počáteční_inventář]
        self.artefakty = []
        self.svět = svet.Svět()
        self.x, self.y = self.svět.začátek.x, self.svět.začátek.y
        self.zdraví = 100
        self.zlato = 0
        self.zkušenost = 0
        self.zdařilý_zásah = False
        self.mapování = False

    def žije(self):
        return self.zdraví > 0

    def vypiš_inventář(self):
        agent.vypiš_inventář(self)

    def nejlepší_zbraň(self):
        try:
            return max((věc for věc in self.inventář
                        if hasattr(věc, 'útok')),
                       key=lambda zbraň: zbraň.útok)
        except ValueError:
            return

    def jdi(self, rozdíl_x, rozdíl_y):
        self.x += rozdíl_x
        self.y += rozdíl_y

    def jdi_na_sever(self):
        self.jdi(rozdíl_x=0, rozdíl_y=-1)

    def jdi_na_jih(self):
        self.jdi(rozdíl_x=0, rozdíl_y=1)

    def jdi_na_východ(self):
        self.jdi(rozdíl_x=1, rozdíl_y=0)

    def jdi_na_západ(self):
        self.jdi(rozdíl_x=-1, rozdíl_y=0)

    def bojuj(self):
        nepřítel = self.místnost_pobytu().nepřítel
        zbraň = self.nejlepší_zbraň()
        síla_zbraně = zbraň.útok if zbraň else 1
        skutečný_zásah_zbraní = vypocty.s_odchylkou(síla_zbraně)
        self.zdařilý_zásah = (skutečný_zásah_zbraní > síla_zbraně * 1.1
                              and nepřítel.krátké_jméno not in ('troll',
                                                                'dobrodruh'))
        útočný_bonus = min(self.zkušenost // 200, 5)
        skutečný_zásah = min(skutečný_zásah_zbraní + útočný_bonus,
                             nepřítel.zdraví)
        nepřítel.zdraví -= skutečný_zásah
        self.zkušenost += skutečný_zásah
        agent.zpráva_o_útoku(zbraň, nepřítel)
        if self.svět.nepřátelé_pobiti():
            odměna = 200
            self.zkušenost += odměna
            agent.zpráva_o_odměně('zabití všech nepřátel', odměna)

    def má_léky(self):
        return any(isinstance(věc, veci.Lék) for věc in self.inventář)

    def kurýruj_se(self):
        léky = [věc for věc in self.inventář if isinstance(věc, veci.Lék)]

        lék = agent.dialog_léčení(léky)
        if lék is not None:
            self.spotřebuj(lék)

    def spotřebuj(self, lék):
        if lék.speciální:
            self.zdraví += lék.léčivá_síla
        else:
            self.zdraví += min(lék.léčivá_síla, 100 - self.zdraví)
        self.inventář.remove(lék)

    def obchoduj(self):
        self.místnost_pobytu().obchoduj(self)

    def kup(self, věc, prodejce):
        prodejce.inventář.remove(věc)
        self.inventář.append(věc)
        cena = věc.cena
        prodejce.zlato += cena
        self.zlato -= cena

    def prodej(self, věc, kupující):
        self.inventář.remove(věc)
        kupující.inventář.append(věc)
        cena = kupující.výkupní_cena(věc)
        self.zlato += cena
        kupující.zlato -= cena

    def místnost_pobytu(self):
        return self.svět[self.x, self.y]

    def nakresli_mapu(self):
        agent.nakresli_mapu(self.svět, (self.x, self.y))
