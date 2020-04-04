# coding: utf-8

from typing import List, Union

from svet import Svět
from utility import ŠÍŘKA, Barva, vypiš_odstavec, vypiš_barevně, vícebarevně, \
                  uděl_odměnu, vstup_z_možností, s_odchylkou
import veci

PoložkyInventáře = List[Union[veci.Zbraň, veci.Lék]]


class Hráč:
    def __init__(já):
        já.inventář: PoložkyInventáře = [
            veci.Zbraň('Tupý nůž', 5, 13),
            veci.Lék('Bylinkový chleba', 8, 10, 'Bylinkovým chlebem'),
        ]
        já.artefakty = []
        já.svět = Svět()
        já.x, já.y = já.svět.začátek.x, já.svět.začátek.y
        já.zdraví = 100
        já.zlato = 10
        já.zkušenost = 0
        já.zdařilý_zásah = False
        já.mapování = False

    def žije(já):
        return já.zdraví > 0

    def vypiš_věci(já):
        print('Máš u sebe:')
        for věc in já.inventář:
            try:
                vícebarevně('            '
                            f'{věc.název_4_pád} (|útok +{věc.útok}|)',
                            (None, Barva.FIALOVÁ))
            except AttributeError:
                vícebarevně('            '
                            f'{věc.název_4_pád} (|zdraví +{věc.léčivá_síla}|)',
                            (None, Barva.TYRKYS))
        for artefakt in já.artefakty:
            vypiš_barevně(f'            < {artefakt} >', barva=artefakt.barva)

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
        nejlepší_zbraň = já.nejlepší_zbraň()
        if nejlepší_zbraň:
            síla_zbraně = nejlepší_zbraň.útok
            název_zbraně = nejlepší_zbraň.název_4_pád
            název_zbraně = název_zbraně[0].lower() + název_zbraně[1:]
        else:
            síla_zbraně = 1
            název_zbraně = 'pěsti'
        skutečný_zásah_zbraní = s_odchylkou(síla_zbraně)
        já.zdařilý_zásah = (skutečný_zásah_zbraní > síla_zbraně * 1.1
                            and nepřítel.krátké_jméno not in ('troll',
                                                              'dobrodruh'))
        útočný_bonus = min(já.zkušenost // 200, 5)
        skutečný_zásah = min(skutečný_zásah_zbraní + útočný_bonus,
                             nepřítel.zdraví)
        nepřítel.zdraví -= skutečný_zásah
        já.zkušenost += skutečný_zásah
        zpráva = (f'Použil jsi {název_zbraně} proti'
                  f' {nepřítel.jméno_3_pád.lower()}.')
        if not nepřítel.žije():
            zpráva += f' Zabil jsi {nepřítel.jméno_4_pád.lower()}!'
        vypiš_odstavec(zpráva, 'boj')
        if já.svět.nepřátelé_pobiti():
            uděl_odměnu(já, 200, 'zabití všech nepřátel')

    def má_léky(já):
        return any(isinstance(věc, veci.Lék) for věc in já.inventář)

    def kurýruj_se(já):
        léky = [věc for věc in já.inventář if isinstance(věc, veci.Lék)]

        print('Čím se chceš kurýrovat?')
        for číslo, věc in enumerate(léky, 1):
            print(f'{číslo:3}. ', end='')
            vícebarevně(f'{věc.název_7_pád} (|zdraví +{věc.léčivá_síla}|)',
                        (None, Barva.TYRKYS))

        while True:
            vícebarevně('Číslo položky             (|Enter| = návrat)',
                        (Barva.MODRÁ, None), konec=' ')
            možnosti = set(range(1, len(léky) + 1))
            vstup = vstup_z_možností(možnosti | {''})
            if vstup == '':
                return
            else:
                lék = léky[vstup - 1]
                já.spotřebuj(lék)
                if lék.léčivá_síla == 90:
                    print('Zmocnil se tě prchavý pocit nadlidské síly a'
                          ' nepřemožitelnosti.')
                else:
                    print('Hned se cítíš líp.')
                return

    def spotřebuj(já, lék):
        if lék.léčivá_síla == 90:
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
        return já.svět.místnost_na_pozici(já.x, já.y)

    def nakresli_mapu(já):
        mapa_navštívených = já.svět.mapa_navštívených((já.x, já.y))

        print('\n'.join(''.join(řádka).center(ŠÍŘKA)
                        for řádka in mapa_navštívených))
        vícebarevně('\n[ |+| les           |#| jeskyně         '
                    '|H| hráč            |?| neznámo ]', (Barva.MODRÁ, None))
