# coding: utf-8

from typing import List, Union

import items
from utils import ŠÍŘKA, Color, vypiš_odstavec, vypiš_barevně, multicolor, \
                  uděl_odměnu, option_input, oscillate
from world import Svět

InventoryList = List[Union[items.Zbraň, items.Léčivka]]


class Hráč:
    def __init__(self):
        self.inventář: InventoryList = [
            items.Zbraň('Tupý nůž', 5, 13),
            items.Léčivka('Bylinkový chleba', 8, 10, 'Bylinkovým chlebem'),
        ]
        self.artefakty = []
        self.svět = Svět()
        self.x, self.y = self.svět.start.x, self.svět.start.y
        self.zdraví = 100
        self.zlato = 10
        self.xp = 0
        self.zdařilý_zásah = False

    def žije(self):
        return self.zdraví > 0

    def vypiš_věci(self):
        print('Máš u sebe:')
        for věc in self.inventář:
            print(f'            {věc}')
        for artefakt in self.artefakty:
            vypiš_barevně(f'            < {artefakt} >', barva=artefakt.barva)

    def nejlepší_zbraň(self):
        try:
            return max((věc for věc in self.inventář
                        if hasattr(věc, 'útok')),
                       key=lambda zbraň: zbraň.útok)
        except ValueError:
            return

    def jdi(self, dx, dy):
        self.x += dx
        self.y += dy

    def jdi_na_sever(self):
        self.jdi(dx=0, dy=-1)

    def jdi_na_jih(self):
        self.jdi(dx=0, dy=1)

    def jdi_na_východ(self):
        self.jdi(dx=1, dy=0)

    def jdi_na_západ(self):
        self.jdi(dx=-1, dy=0)

    def bojuj(self):
        nepřítel = self.místnost_pobytu().nepřítel
        nejlepší_zbraň = self.nejlepší_zbraň()
        if nejlepší_zbraň:
            síla_zbraně = nejlepší_zbraň.útok
            název_zbraně = nejlepší_zbraň.název_4_pád.lower()
        else:
            síla_zbraně = 1
            název_zbraně = 'pěsti'
        skutečný_zásah_zbraní = oscillate(síla_zbraně)
        self.zdařilý_zásah = (skutečný_zásah_zbraní > síla_zbraně * 1.1
                              and nepřítel.krátké_jméno not in ('troll',
                                                                'dobrodruh'))
        útočný_bonus = self.xp // 200
        skutečný_zásah = min(skutečný_zásah_zbraní + útočný_bonus,
                             nepřítel.zdraví)
        nepřítel.zdraví -= skutečný_zásah
        self.xp += skutečný_zásah
        zpráva = (f'Použil jsi {název_zbraně} proti'
                  f' {nepřítel.jméno_3_pád.lower()}.')
        if not nepřítel.žije():
            zpráva += f' Zabil jsi {nepřítel.jméno_4_pád.lower()}!'
        vypiš_odstavec(zpráva, 'boj')
        if self.svět.nepřátelé_pobiti():
            uděl_odměnu(self, 200, 'zabití všech nepřátel')

    def má_léčivky(self):
        return any(isinstance(věc, items.Léčivka)
                   for věc in self.inventář)

    def kurýruj_se(self):
        léčivky = [věc for věc in self.inventář
                   if isinstance(věc, items.Léčivka)]

        print('Čím se chceš kurýrovat?')
        for i, věc in enumerate(léčivky, 1):
            print(f'{i:3}. ', end='')
            vypiš_barevně(f'{věc.str_7()}', barva=Color.CYAN)

        while True:
            multicolor('Číslo položky             (|Enter| = návrat)',
                       (Color.BLUE, None), end=' ')
            možnosti = set(range(1, len(léčivky) + 1))
            vstup = option_input(možnosti | {''})
            if vstup == '':
                return
            else:
                vybráno = léčivky[vstup - 1]
                self.zdraví = min(100, self.zdraví + vybráno.léčivá_síla)
                self.inventář.remove(vybráno)
                print('Hned se cítíš líp.')
                return

    def obchoduj(self):
        self.místnost_pobytu().obchoduj(self)

    def místnost_pobytu(self):
        return self.svět.místnost_na_pozici(self.x, self.y)

    def nakresli_mapu(self):
        mapa_navštívených = self.svět.mapa_navštívených((self.x, self.y))

        print('\n'.join(''.join(řádka).center(ŠÍŘKA)
                        for řádka in mapa_navštívených))
        multicolor('\n[ |+| les           |#| jeskyně         '
                   '|H| hráč            |?| neznámo ]', (Color.BLUE, None))
