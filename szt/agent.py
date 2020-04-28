# coding: utf-8

"""
Zprostředkovatel mezi vnitřní logikou hry (submoduly `hra`, `hrac`,
`svet`, `nepratele`, `postavy`, `veci`, `utility` a `data`) a rozhraním
viditelným pro uživatele (submoduly `dialogy`, `konzole` a `barvy`).

Moduly z první skupiny by neměly napřímo importovat moduly z druhé
skupiny a naopak.
"""

from . import dialogy, konzole

vstup_číslo_položky = dialogy.vstup_číslo_položky
vstup_koupit_prodat = dialogy.vstup_koupit_prodat
potvrď_konec = dialogy.potvrď_konec
dialog_léčení = dialogy.dialog_léčení

vypiš_odstavec = konzole.vypiš_odstavec
piš = konzole.piš
zobraz_titul = konzole.zobraz_titul
vypiš_úvodní_text = konzole.vypiš_úvodní_text
zobraz_gratulaci = konzole.zobraz_gratulaci
nerozumím = konzole.nerozumím
vypiš_název_akce = konzole.vypiš_název_akce
vypiš_popis_místnosti = konzole.vypiš_popis_místnosti
nakresli_mapu = konzole.nakresli_mapu
stav_hráče = konzole.stav_hráče
vypiš_věc_v_obchodě = konzole.vypiš_věc_v_obchodě
vypiš_inventář = konzole.vypiš_inventář
zobraz_možnosti = konzole.zobraz_možnosti
uděl_odměnu = konzole.uděl_odměnu
zpráva_o_útoku = konzole.zpráva_o_útoku
zpráva_zdařilý_zásah = konzole.zpráva_zdařilý_zásah
zpráva_o_zranění = konzole.zpráva_o_zranění
zpráva_kořist_zlato = konzole.zpráva_kořist_zlato
zpráva_kořist_zbraň = konzole.zpráva_kořist_zbraň
