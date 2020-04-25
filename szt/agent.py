# coding: utf-8

"""
Zprostředkovatel mezi vnitřní logikou hry (submoduly `hra`, `hrac`,
`svet`, `nepratele`, `postavy`, `veci`, `utility` a `data`) a rozhraním
viditelným pro uživatele (submoduly `dialogy`, `konzole` a `barvy`).

Moduly z první skupiny by neměly napřímo importovat moduly z druhé
skupiny a naopak.
"""

from . import dialogy, konzole

potvrď_konec = dialogy.potvrď_konec
vstup_číslo_položky = dialogy.vstup_číslo_položky
vstup_koupit_prodat = dialogy.vstup_koupit_prodat
dialog_léčení = dialogy.dialog_léčení

zobraz_možnosti = konzole.zobraz_možnosti
stav_hráče = konzole.stav_hráče
vypiš_název_akce = konzole.vypiš_název_akce
nerozumím = konzole.nerozumím
vypiš_odstavec = konzole.vypiš_odstavec
vypiš_barevně = konzole.vypiš_barevně
uděl_odměnu = konzole.uděl_odměnu
nakresli_mapu = konzole.nakresli_mapu
zobraz_titul = konzole.zobraz_titul
zobraz_gratulaci = konzole.zobraz_gratulaci
vypiš_věc_v_obchodě = konzole.vypiš_věc_v_obchodě
vypiš_inventář = konzole.vypiš_inventář
vypiš_úvodní_text = konzole.vypiš_úvodní_text
zpráva_o_útoku = konzole.zpráva_o_útoku
