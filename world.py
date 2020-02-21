# coding: utf-8

import random

import enemies
import items
import npc
from utils import WIDTH, Color, nice_print, color_print, multicolor, \
    award_bonus, option_input, oscillate, okolí


class Místnost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.navštívena = False
        self.viděna = False

    def dopad_na_hráče(self, hráč):
        pass

    def popis(self):
        return self.text


class Jeskyně(Místnost):
    def __init__(self, x, y):
        super().__init__(x, y)
        if x <= 18 and y <= 6:
            # zone 1
            self.text = ('Klopýtáš po rozbitém kamení v téměř úplné tmě této'
                         ' části jeskyně.')
        elif x >= 27 and y <= 7:
            # zone 3
            self.text = ('Našlapuješ po rozměklé zemi ve vlhké a zatuchlé části'
                         ' jeskyně.')
        elif 22 <= x <= 26 and y >= 9:
            # zone 5
            self.text = 'Procházíš chladnou tmavou jeskyní.'
        elif x >= 27 and y >= 9:
            # zone 6
            self.text = 'Procházíš spletí nepříjemně tísnivých úzkých chodeb.'
        elif x <= 8 and y >= 18:
            # zone 8
            self.text = 'Procházíš chladnou tmavou jeskyní.'
        elif y >= 19:
            # zone 9
            self.text = 'Procházíš chladnou tmavou jeskyní.'
        elif x <= 11 and y >= 10:
            # zone 7
            self.text = 'Procházíš chladnou tmavou jeskyní.'
        elif x <= 21 and y >= 7:
            # zone 4
            self.text = 'Procházíš chladnou tmavou jeskyní.'
        else:
            # zone 2
            self.text = 'Procházíš chladnou tmavou jeskyní.'


class Les(Místnost):
    def __init__(self, x, y):
        super().__init__(x, y)
        if x <= 8 and y <= 14:
            self.text = ('Jdeš po sotva znatelné stezce vedoucí tmavým a'
                         ' zlověstně tichým lesem. V pološeru zakopáváš o'
                         ' kořeny obrovských stromů.')
        elif 14 <= x <= 20 and 14 <= y <= 20:
            self.text = 'Procházíš nejtmavší a nejponurejší částí lesa.'
        else:
            self.text = 'Jdeš po úzké, zarostlé lesní pěšině.'


class MístnostBoj(Místnost):
    def __init__(self, x, y, nepřítel):
        super().__init__(x, y)
        self.nepřítel = nepřítel

    def popis(self):
        return self.text + ' ' + self.nepřítel.text

    def dopad_na_hráče(self, hráč):
        if self.nepřítel.žije():
            if hráč.zdařilý_zásah:
                nice_print(f'Zasáhl jsi {self.nepřítel.jméno_4_pád.lower()} do'
                           f' hlavy. {self.nepřítel.jméno} zmateně vrávorá.',
                           'fight', Color.BLUE)
            else:
                skutečný_zásah_nepřítele = oscillate(self.nepřítel.útok)
                obranný_bonus = hráč.xp // 200
                skutečný_zásah = min(skutečný_zásah_nepřítele - obranný_bonus,
                                     hráč.zdraví)
                hráč.zdraví -= max(skutečný_zásah, 0)
                zpráva = f'{self.nepřítel} útočí. '
                if hráč.žije():
                    zpráva += ('Utrpěl jsi zranění.' if skutečný_zásah > 0
                               else 'Ubránil ses.')
                    hráč.xp += 1
                else:
                    zpráva += f'{random.choice(("Ouha", "Běda"))}, jsi mrtev!'
                nice_print(zpráva, 'fight', Color.RED)
        else:
            try:
                if not self.nepřítel.zlato_sebráno and self.nepřítel.zlato > 0:
                    self.nepřítel.zlato_sebráno = True
                    hráč.zlato += self.nepřítel.zlato
                    zpráva = (f'Sebral jsi {self.nepřítel.jméno_3_pád.lower()}'
                              f' {self.nepřítel.zlato} zlaťáků.')
                    nice_print(zpráva, 'luck')
                if not self.nepřítel.zbraň_sebrána:
                    self.nepřítel.weapon_claimed = True
                    hráč.inventář.append(self.nepřítel.zbraň)
                    zpráva = (f'Sebral jsi {self.nepřítel.jméno_3_pád.lower()}'
                              f' {self.nepřítel.zbraň.name_4.lower()}.')
                    nice_print(zpráva, 'luck')
            except AttributeError:
                pass


class JeskyněBoj(MístnostBoj, Jeskyně):
    pass


class LesBoj(MístnostBoj, Les):
    pass


class JeskyněObchod(Jeskyně):
    def __init__(self, x, y, obchodník):
        super().__init__(x, y)
        self.text = 'Stojíš u vchodu do jeskyně.'
        self.obchodník = obchodník

    def proveď_obchod(self, kupující, prodejce):
        věci_na_prodej = [věc for věc in prodejce.inventář
                          if věc.value is not None]
        if not věci_na_prodej:
            print(f'{prodejce.jméno} už nemá co nabídnout.'
                  if prodejce is self.obchodník
                  else 'Nemáš nic, co bys mohl prodat.')
            return
        else:
            print(f'{prodejce.jméno} nabízí tyto věci:'
                  if prodejce is self.obchodník
                  else 'Tyto věci můžeš prodat:')

        možnosti = set()
        for i, věc in enumerate(věci_na_prodej, 1):
            cena = (kupující.výkupní_cena(věc) if kupující is self.obchodník
                    else věc.value)
            if cena <= kupující.zlato:
                možnosti.add(i)
                číslo_položky = f'{i:3}.'
            else:
                číslo_položky = '    '
            print(f'{číslo_položky} ', end='')
            color_print(f'{věc} '.ljust(WIDTH - 25, '.')
                        + f' {cena:3} zlaťáků', color=Color.CYAN)

        try:
            název_peněz, oslovení = kupující.mluva
        except AttributeError:
            název_peněz, oslovení = prodejce.mluva

        if not možnosti:
            print(f'"Došly mi {název_peněz}, {oslovení}!"'
                  f' říká {kupující.jméno.lower()}.'
                  if kupující is self.obchodník
                  else 'Na žádnou z nich nemáš peníze.')
            return

        while True:
            multicolor('Číslo položky             (|Enter| = návrat)',
                       (Color.BLUE, None), end=' ')
            vstup = option_input(možnosti | {''})
            if vstup == '':
                return
            else:
                vybráno = prodejce.inventář[vstup - 1]
                prodejce.inventář.remove(vybráno)
                kupující.inventář.append(vybráno)
                cena = (kupující.výkupní_cena(vybráno)
                        if kupující is self.obchodník
                        else vybráno.value)
                prodejce.zlato += cena
                kupující.zlato -= cena
                print(f'"Bylo mi potěšením, {oslovení}."'
                      f' říká {self.obchodník.name.lower()}.')
                return

    def obchoduj(self, hráč):
        while True:
            multicolor('K|: koupit    |P|: prodat    (|Enter| = návrat)',
                       (None, Color.BLUE), end=' ')
            vstup = option_input({'K', 'P', ''})
            if vstup == '':
                return
            elif vstup == 'K':
                kupující, prodejce = hráč, self.obchodník
            else:
                kupující, prodejce = self.obchodník, hráč
            self.proveď_obchod(kupující=kupující, prodejce=prodejce)

    def popis(self):
        return self.text + ' ' + self.obchodník.text


class JeskyněZlato(Jeskyně):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.zlato = random.randint(12, 24)
        self.zlato_sebráno = False

    def dopad_na_hráče(self, hráč):
        if not self.zlato_sebráno:
            self.zlato_sebráno = True
            hráč.zlato += self.zlato
            zpráva = f'Našel jsi {self.zlato} zlaťáků.'
            nice_print(zpráva, 'luck')


class JeskyněArtefakt(Jeskyně):
    def __init__(self, x, y, artefakt):
        super().__init__(x, y)
        self.artefakt = artefakt
        self.artefakt_sebrán = False

    def dopad_na_hráče(self, hráč):
        if not self.artefakt_sebrán:
            self.artefakt_sebrán = True
            hráč.artefakty.append(self.artefakt)
            zpráva = f'Našel jsi {self.artefakt.name_4.lower()}.'
            nice_print(zpráva, 'luck')
            if hráč.svět.poklad_posbírán():
                award_bonus(hráč, 300, 'nalezení všech magických předmětů')
                nice_print('Artefakty teď musíš vynést ven z jeskyně a dojít'
                           ' s nimi na začátek své cesty.')
                hráč.svět.start.text += (
                    ' Překonal jsi všechny nástrahy a skutečně se ti podařilo'
                    ' získat kýžené magické artefakty. Otevírá se před tebou'
                    ' svět neomezených možností.'
                )


class MístnostZbraň(Místnost):
    def __init__(self, x, y):
        super().__init__(x, y)
        if (x, y) == (27, 23):
            parametry = ('Rezavá dýka', 9, 31, 'Rezavou dýku')
        elif (x, y) == (15, 18):
            parametry = ('Zrezivělý meč', 16, 69)
        else:
            parametry = random.choice((('Ostnatý palcát', 18, 82),
                                       ('Řemdih', 20, 91)))
        self.zbraň = items.Weapon(*parametry)
        self.zbraň_sebrána = False

    def dopad_na_hráče(self, hráč):
        if not self.zbraň_sebrána:
            self.zbraň_sebrána = True
            hráč.inventář.append(self.zbraň)
            if isinstance(self, Les):
                zpráva = ('V křoví u cesty jsi našel'
                          f' {self.zbraň.name_4.lower()}.')
            else:
                zpráva = ('Ve skulině pod kamenem jsi našel'
                          f' {self.zbraň.name_4.lower()}.')
            nice_print(zpráva, 'luck')


class JeskyněZbraň(MístnostZbraň, Jeskyně):
    pass


class LesZbraň(MístnostZbraň, Les):
    pass


class LesLéčivka(Les):
    def __init__(self, x, y):
        super().__init__(x, y)
        if (x, y) == (34, 23):
            parametry = ('Léčivé bylinky', 18, 19, 'Léčivými bylinkami')
        elif (x, y) == (30, 25):
            parametry = ('Léčivé houby', 12, 9, 'Léčivými houbami')
        elif (x, y) == (31, 18):
            parametry = ('Léčivé bobule', 13, 11, 'Léčivými bobulemi')
        else:
            parametry = random.choice((
                ('Léčivé houby', 12, 9, 'Léčivými houbami'),
                ('Léčivé bobule', 13, 11, 'Léčivými bobulemi'),
                ('Léčivé bylinky', 18, 19, 'Léčivými bylinkami'),
                ('Kouzelné houby', 22, 25, 'Kouzelnými houbami'),
                ('Kouzelné bobule', 16, 16, 'Kouzelnými bobulemi'),
            ))
        self.léčivka = items.Consumable(*parametry)
        self.léčivka_sebrána = False

    def dopad_na_hráče(self, hráč):
        if not self.léčivka_sebrána:
            self.léčivka_sebrána = True
            hráč.inventář.append(self.léčivka)
            zpráva = f'Našel jsi {self.léčivka.name_4.lower()}.'
            nice_print(zpráva, 'luck')


mapa_hry = '''
fm        gc cccc A                      
 fff    cc C c  Ccc                      
  f      cccccc    c         gc          
  F  f        cHcc c c  cg    C cc       
 ff fFf   ccC c  cccccc c    cc  cccg    
 f  f f   c ccc  c   T  c  cTc ccC       
 ff f m f A   c  cc cccccccc ccc c       
f fff fff   c          C  C      cA      
f F m   fW  c  cgcc c ccccccc            
fmf      cccc  c  c ccc       c  g c     
f ff    c   cCcc cCcc C g   ccc  c cc    
ff f   Cccccc  ccc  c c c ccc  c ccc     
 F m  cc  c cgCc c wc cccCc cTcccc       
mf    g  cc c       c c  c    c  cCc     
 ff   cc c        f   g cc    gc   w     
         T    Ffm f     c                
         cg   f  ffff   M                
         c c  ffff t    f           ff f 
       ccCcc   x   f mf f ffff m     ffff
   cc cc  c       mf  fff  f fff  ff f  m
    c  c ccCc cc   fff  fFff   F   fFff  
    cccc c  c  cA    F  f  m fff fff  ff 
   Cc g  c ccc C     fffff   f   f  f f  
   c  c  c w ccc     m f f xffFf fm ffFff
   cA                  f f  f  fff  f   f
                            ffm  f fm fff
                                 f f ff f
                                 S     mf
'''


class Svět:
    def __init__(self):
        self.mapa = []
        self.start = None
        self.načti_mapu(mapa_hry)

    def místnost_na_pozici(self, x, y):
        if x < 0 or y < 0:
            return None
        try:
            return self.mapa[y][x]
        except IndexError:
            return None

    def načti_mapu(self, mapa):
        data_artefaktů = {
            ('Křišťálová koule', None, 'Křišťálovou kouli'),
            ('Rubínový kříž', Color.RED),
            ('Tyrkysová tiára', Color.CYAN, 'Tyrkysovou tiáru'),
            ('Ametystový kalich', Color.MAGENTA),
            ('Safírový trojzubec', Color.BLUE)
        }

        if mapa.count('1') > len(data_artefaktů):
            raise ValueError('Nedostatek dat pro artefakty')
        if mapa.count('S') != 1:
            raise ValueError('Na mapě musí být přesně jedna startovní místnost')

        řádky = mapa.strip('\n').splitlines()
        for y, řádka in enumerate(řádky):
            řádka_mapy = []
            for x, kód_místnosti in enumerate(řádka):
                typ_místnosti = {'c': Jeskyně,
                                 'f': Les,
                                 'C': JeskyněBoj,
                                 'F': LesBoj,
                                 't': LesBoj,
                                 'T': JeskyněBoj,  # troll
                                 'H': JeskyněBoj,  # člověk
                                 'S': Les,
                                 'g': JeskyněZlato,
                                 'A': JeskyněArtefakt,
                                 'w': JeskyněZbraň,
                                 'x': LesZbraň,
                                 'm': LesLéčivka,
                                 'M': JeskyněObchod,  # mastičkář
                                 'W': JeskyněObchod,  # zbrojíř
                                 ' ': None}[kód_místnosti]

                parametry = {}
                if kód_místnosti == 'M':
                    parametry.update(obchodník=npc.Obchodník.mastičkář())
                elif kód_místnosti == 'W':
                    parametry.update(obchodník=npc.Obchodník.zbrojíř())
                elif kód_místnosti == 'C':
                    parametry.update(
                        nepřítel=enemies.náhodný_jeskynní_nepřítel()
                    )
                elif kód_místnosti == 'F':
                    parametry.update(nepřítel=enemies.náhodný_lesní_nepřítel())
                elif kód_místnosti == 't':
                    parametry.update(nepřítel=enemies.Netvor.lesní_troll())
                elif kód_místnosti == 'T':
                    parametry.update(nepřítel=enemies.Netvor.troll())
                elif kód_místnosti == 'H':
                    parametry.update(nepřítel=enemies.Člověk.dobrodruh())
                elif kód_místnosti == 'A':
                    parametry.update(
                        artefakt=items.Artifact(*data_artefaktů.pop())
                    )

                if typ_místnosti:
                    místnost = typ_místnosti(x, y, **parametry)
                    řádka_mapy.append(místnost)
                    if kód_místnosti == 'S':
                        místnost.text = (
                            'Stojíš při okraji tajuplného lesa na úpatí'
                            ' nehostinné Hory běsů. Vrchol jejího hrozivého'
                            ' štítu je zahalen nízkým mračnem.'
                        )
                        self.start = místnost
                else:
                    řádka_mapy.append(None)

            self.mapa.append(řádka_mapy)

    def poklad_posbírán(self):
        return all(místnost.artefakt_sebrán for místnost in self
                   if hasattr(místnost, 'artefakt_sebrán'))

    def nepřátelé_pobiti(self):
        return not any(místnost.nepřítel.žije() for místnost in self
                       if hasattr(místnost, 'nepřítel'))

    def vše_navštíveno(self):
        return all(místnost.navštívena for místnost in self)

    def mapa_navštívených(self, pozice_hráče):
        mapa = []
        ořez_vlevo, ořez_vpravo = 1000, 1000
        for řádka in self.mapa:
            řádka_mapy = []
            for místnost in řádka:
                try:
                    if (místnost.x, místnost.y) == pozice_hráče:
                        řádka_mapy.append('H')
                    elif místnost.navštívena:
                        řádka_mapy.append('#' if isinstance(místnost, Jeskyně)
                                          else '+')
                    elif místnost.viděna:
                        řádka_mapy.append('?')
                    else:
                        řádka_mapy.append(' ')
                except AttributeError:
                    řádka_mapy.append(' ')
            if set(řádka_mapy) != {' '}:
                prázdno_vlevo, prázdno_vpravo = okolí(''.join(řádka_mapy), ' ')
                ořez_vlevo = min(ořez_vlevo, prázdno_vlevo)
                ořez_vpravo = min(ořez_vpravo, prázdno_vpravo)
                mapa.append(řádka_mapy)

        for řádka_mapy in mapa:
            řádka_mapy[:ořez_vlevo] = []
            řádka_mapy[len(řádka_mapy) - ořez_vpravo:] = []

        return mapa

    def __iter__(self):
        return iter(místnost for řádka in self.mapa for místnost in řádka
                    if místnost is not None)
