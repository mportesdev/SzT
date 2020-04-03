# coding: utf-8

import math
import random

import nepratele
import postavy
from utility import ŠÍŘKA, Barva, vypiš_odstavec, vypiš_barevně, vícebarevně, \
                  uděl_odměnu, vstup_z_možností, s_odchylkou, okraje
import veci


class Místnost:
    def __init__(já, x, y):
        já.x = x
        já.y = y
        já.navštívena = False
        já.viděna = False

    def dopad_na_hráče(já, hráč):
        pass

    def popis(já):
        return já.text


class Jeskyně(Místnost):
    def __init__(já, x, y):
        super().__init__(x, y)

        texty = (
            'Procházíš spletí nepříjemně tísnivých podzemních chodeb.',
            'Našlapuješ po rozměklé zemi ve vlhké a zatuchlé jeskyni.',
            'Jdeš vlhkou a chladnou jeskyní.',
            'Procházíš zapáchajícími jeskynními chodbami.',
            'Jdeš špinavými štolami s těžko dýchatelným vzduchem.',
            'Klopýtáš v téměř dokonalé temnotě této části jeskyně.',
        )
        já.text = texty[já.zóna()]

    def zóna(já):
        vzdálenost_od_středu = math.hypot(já.x - 18, já.y - 10)
        return min(int(vzdálenost_od_středu / 3), 5)


class Les(Místnost):
    def __init__(já, x, y):
        super().__init__(x, y)

        texty = (
            'Kráčíš zlověstným tichem zšeřelého lesa.',
            'Jdeš po úzké, zarostlé lesní pěšině.',
            'Procházíš nejtmavší a nejponuřejší částí lesa.',
            'Jdeš po sotva znatelné lesní stezce.',
            'Procházíš hustým porostem prastarého lesa.',
        )
        já.text = texty[já.zóna()]

    def zóna(já):
        vzdálenost_od_středu = math.hypot(já.x - 18, já.y - 10)
        return int(vzdálenost_od_středu / 3) // 2


class MístnostBoj(Místnost):
    def __init__(já, x, y, nepřítel):
        super().__init__(x, y)
        já.nepřítel = nepřítel

    def popis(já):
        return já.text + ' ' + já.nepřítel.text

    def dopad_na_hráče(já, hráč):
        if já.nepřítel.žije():
            if hráč.zdařilý_zásah:
                vypiš_odstavec(
                    f'Zasáhl jsi {já.nepřítel.jméno_4_pád.lower()} do hlavy.'
                    f' {já.nepřítel.jméno} zmateně vrávorá.',
                    'boj', Barva.MODRÁ
                )
            else:
                skutečný_zásah_nepřítele = s_odchylkou(já.nepřítel.útok)
                obranný_bonus = min(hráč.zkušenost // 200, 5)
                skutečný_zásah = min(skutečný_zásah_nepřítele - obranný_bonus,
                                     hráč.zdraví)
                hráč.zdraví -= max(skutečný_zásah, 0)
                zpráva = f'{já.nepřítel} útočí. '
                if hráč.žije():
                    zpráva += ('Utrpěl jsi zranění.' if skutečný_zásah > 0
                               else 'Ubránil ses.')
                    hráč.zkušenost += 1
                else:
                    zpráva += f'{random.choice(("Ouha", "Běda"))}, jsi mrtev!'
                vypiš_odstavec(zpráva, 'boj', Barva.ČERVENÁ)
        else:
            try:
                if not já.nepřítel.zlato_sebráno and já.nepřítel.zlato > 0:
                    já.nepřítel.zlato_sebráno = True
                    hráč.zlato += já.nepřítel.zlato
                    zpráva = (f'Sebral jsi {já.nepřítel.jméno_3_pád.lower()}'
                              f' {já.nepřítel.zlato} zlaťáků.')
                    vypiš_odstavec(zpráva, 'štěstí')
                if not já.nepřítel.zbraň_sebrána:
                    já.nepřítel.zbraň_sebrána = True
                    hráč.inventář.append(já.nepřítel.zbraň)
                    zpráva = (f'Sebral jsi {já.nepřítel.jméno_3_pád.lower()}'
                              f' {já.nepřítel.zbraň.název_4_pád.lower()}.')
                    vypiš_odstavec(zpráva, 'štěstí')
            except AttributeError:
                pass


class JeskyněBoj(MístnostBoj, Jeskyně):
    pass


class LesBoj(MístnostBoj, Les):
    pass


class JeskyněObchod(Jeskyně):
    def __init__(já, x, y, obchodník):
        super().__init__(x, y)
        já.text = 'Stojíš u vchodu do jeskyně.'
        já.obchodník = obchodník

    def proveď_obchod(já, kupující, prodejce):
        věci_na_prodej = [věc for věc in prodejce.inventář
                          if věc.cena is not None]
        if not věci_na_prodej:
            print(f'{prodejce.jméno} už nemá co nabídnout.'
                  if prodejce is já.obchodník
                  else 'Nemáš nic, co bys mohl prodat.')
            return
        else:
            print(f'{prodejce.jméno} nabízí tyto věci:'
                  if prodejce is já.obchodník
                  else 'Tyto věci můžeš prodat:')

        možnosti = set()
        for číslo, věc in enumerate(věci_na_prodej, 1):
            cena = (kupující.výkupní_cena(věc) if kupující is já.obchodník
                    else věc.cena)
            if cena <= kupující.zlato:
                možnosti.add(číslo)
                číslo_položky = f'{číslo:3}.'
            else:
                číslo_položky = '    '
            print(f'{číslo_položky} ', end='')
            try:
                vícebarevně(
                    f'{věc.název_4_pád}'
                    f' (|útok +{věc.útok}|) '.ljust(ŠÍŘKA - 25, '.')
                    + f' {cena:3} zlaťáků',
                    (None, Barva.FIALOVÁ)
                )
            except AttributeError:
                vícebarevně(
                    f'{věc.název_4_pád}'
                    f' (|zdraví +{věc.léčivá_síla}|) '.ljust(ŠÍŘKA - 25, '.')
                    + f' {cena:3} zlaťáků',
                    (None, Barva.TYRKYS)
                )

        try:
            název_peněz, oslovení = kupující.mluva
        except AttributeError:
            název_peněz, oslovení = prodejce.mluva

        if not možnosti:
            print(f'"Došly mi {název_peněz}, {oslovení}!"'
                  f' říká {kupující.jméno.lower()}.'
                  if kupující is já.obchodník
                  else 'Na žádnou z nich nemáš peníze.')
            return

        while True:
            vícebarevně('Číslo položky             (|Enter| = návrat)',
                        (Barva.MODRÁ, None), konec=' ')
            vstup = vstup_z_možností(možnosti | {''})
            if vstup == '':
                return
            else:
                vybraná_věc = prodejce.inventář[vstup - 1]
                if prodejce is já.obchodník:
                    kupující.kup(vybraná_věc, prodejce)
                else:
                    prodejce.prodej(vybraná_věc, kupující)
                print(f'"Bylo mi potěšením, {oslovení}."'
                      f' říká {já.obchodník.jméno.lower()}.')
                return

    def obchoduj(já, hráč):
        while True:
            vícebarevně('K|: koupit    |P|: prodat    (|Enter| = návrat)',
                        (None, Barva.MODRÁ), konec=' ')
            vstup = vstup_z_možností({'K', 'P', ''})
            if vstup == '':
                return
            elif vstup == 'K':
                kupující, prodejce = hráč, já.obchodník
            else:
                kupující, prodejce = já.obchodník, hráč
            já.proveď_obchod(kupující=kupující, prodejce=prodejce)

    def popis(já):
        return já.text + ' ' + já.obchodník.text


class JeskyněZlato(Jeskyně):
    def __init__(já, x, y):
        super().__init__(x, y)
        já.zlato = random.randint(12, 24)
        já.zlato_sebráno = False

    def dopad_na_hráče(já, hráč):
        if not já.zlato_sebráno:
            já.zlato_sebráno = True
            hráč.zlato += já.zlato
            vypiš_odstavec(f'Našel jsi {já.zlato} zlaťáků.', 'štěstí')


class JeskyněArtefakt(Jeskyně):
    def __init__(já, x, y, artefakt):
        super().__init__(x, y)
        já.artefakt = artefakt
        já.artefakt_sebrán = False

    def dopad_na_hráče(já, hráč):
        if not já.artefakt_sebrán:
            já.artefakt_sebrán = True
            hráč.artefakty.append(já.artefakt)
            vypiš_odstavec(f'Našel jsi {já.artefakt.název_4_pád.lower()}.',
                           'štěstí')
            if hráč.svět.poklad_posbírán():
                uděl_odměnu(hráč, 300, 'nalezení všech magických předmětů')
                vypiš_odstavec('Artefakty teď musíš vynést ven z jeskyně a'
                               ' dojít s nimi na začátek své cesty.')


class MístnostZbraň(Místnost):
    def __init__(já, x, y, zbraň):
        super().__init__(x, y)
        já.zbraň = zbraň
        já.zbraň_sebrána = False

    def dopad_na_hráče(já, hráč):
        if not já.zbraň_sebrána:
            já.zbraň_sebrána = True
            hráč.inventář.append(já.zbraň)
            if isinstance(já, Les):
                zpráva = ('V křoví u cesty jsi našel'
                          f' {já.zbraň.název_4_pád.lower()}.')
            else:
                zpráva = ('Ve skulině pod kamenem jsi našel'
                          f' {já.zbraň.název_4_pád.lower()}.')
            vypiš_odstavec(zpráva, 'štěstí')


class JeskyněZbraň(MístnostZbraň, Jeskyně):
    pass


class LesZbraň(MístnostZbraň, Les):
    pass


class MístnostLék(Místnost):
    def __init__(já, x, y, lék):
        super().__init__(x, y)
        já.lék = lék
        já.lék_sebrán = False

    def dopad_na_hráče(já, hráč):
        if not já.lék_sebrán:
            já.lék_sebrán = True
            hráč.inventář.append(já.lék)
            if isinstance(já, Les):
                zpráva = (f'Našel jsi {já.lék.název_4_pád.lower()}.')
            else:
                zpráva = ('Na zemi jsi našel zaprášenou'
                          f' {já.lék.název_4_pád.lower()}.')
            vypiš_odstavec(zpráva, 'štěstí')


class JeskyněLék(MístnostLék, Jeskyně):
    pass


class LesLék(MístnostLék, Les):
    pass


mapa_hry = '''
fm        gc cccc A                      
 fff    lc C c  Ccc                      
  f      cccccc    c         gc          
  F  f        cHcc c c  cg    C lc       
 ff fFf   ccC c  cccccc c    cc  cccg    
 f  f f   c ccc  c   T  c  cTc ccC       
 ff f m f A   c  cw cccccccc ccc c       
f fff fff   c          C  C      cA      
f F m   fW  c  cgcc c ccccccc            
fmf      cccc  c  c ccc       c  g c     
f ff    c   cCcc cCcc C g   ccc  c cl    
ff f   Cccccc  ccc  c c c ccc  c ccc     
 F m  cc  c cgCc c wc cccCc cTcccc       
mf    g  cc c       c c  c    c  cCc     
 ff   cc c        f   g cc    gc   w     
         T    Ffm f     c                
         cg   f  ffff   M                
         c c  ffff t    f           ff f 
       ccCcc   x   f mf f ffff m     ffFf
   cc cc  c       mf  fff  f fff  ff f  m
    c  c ccCc lc   fff  fFff   F   fFff  
    cccc c  c  cA    F  f  m fff fff  ff 
   Cc g  c ccc C     fffff   f   f  f f  
   c  c  c w ccc     m f f xffFf fm ffFff
   cA                  f f  f  fff  f   f
                            ffm  f fm fff
                                 f f ff f
                                 S     mf
'''


class Svět:
    def __init__(já):
        já.mapa = []
        já.začátek = None
        já.načti_mapu(mapa_hry)

    def místnost_na_pozici(já, x, y):
        if x < 0 or y < 0:
            return None
        try:
            return já.mapa[y][x]
        except IndexError:
            return None

    def načti_mapu(já, mapa):

        def generátor_zbraní():
            data_zbraní = {
                ('Srp a kladivo', 17, 54),
                ('Ostnatý palcát', 18, 82),
                ('Zkrvavená mačeta', 19, 85, 'Zkrvavenou mačetu'),
            }

            while True:
                if (x, y) == (27, 23):
                    yield veci.Zbraň('Rezavá dýka', 9, 31, 'Rezavou dýku')
                elif (x, y) == (15, 18):
                    yield veci.Zbraň('Zrezivělý meč', 16, 69)
                elif (x, y) == (35, 14):
                    yield veci.Zbraň('Těžká sekera', 26, 117, 'Těžkou sekeru')
                else:
                    yield veci.Zbraň(*data_zbraní.pop())

        def generátor_léků():
            data_léků = {
                ('Léčivé houby', 12, 9, 'Léčivými houbami'),
                ('Léčivé bobule', 13, 11, 'Léčivými bobulemi'),
                ('Léčivé bylinky', 18, 19, 'Léčivými bylinkami'),
                ('Kouzelné houby', 22, 25, 'Kouzelnými houbami'),
                ('Kouzelné bobule', 16, 16, 'Kouzelnými bobulemi'),
                ('Léčivé houby', 14, 12, 'Léčivými houbami'),
                ('Léčivé bobule', 11, 9, 'Léčivými bobulemi'),
                ('Léčivé bylinky', 17, 18, 'Léčivými bylinkami'),
                ('Léčivé bylinky', 17, 17, 'Léčivými bylinkami'),
                ('Kouzelné houby', 22, 24, 'Kouzelnými houbami'),
                ('Kouzelné bobule', 16, 17, 'Kouzelnými bobulemi'),
                ('Kouzelné bylinky', 21, 23, 'Léčivými bylinkami'),
                ('Kouzelné bylinky', 19, 20, 'Léčivými bylinkami'),
                ('Kouzelné bylinky', 19, 21, 'Léčivými bylinkami'),
            }

            while True:
                if (x, y) == (34, 23):
                    yield veci.Lék('Léčivé bylinky', 18, 19, 'Léčivými bylinkami')
                elif (x, y) == (30, 25):
                    yield veci.Lék('Léčivé houby', 12, 9, 'Léčivými houbami')
                elif (x, y) == (31, 18):
                    yield veci.Lék('Léčivé bobule', 13, 11, 'Léčivými bobulemi')
                elif kód_místnosti == 'l':
                    yield veci.Lék('Lahvička medicíny',
                                   random.randint(35, 45), 21,
                                   'Lahvičkou medicíny', 'Lahvičku medicíny')
                else:
                    yield veci.Lék(*data_léků.pop())

        zbraně_iterátor = generátor_zbraní()
        léky_iterátor = generátor_léků()

        data_artefaktů = {
            ('Křišťálová koule', None, 'Křišťálovou kouli'),
            ('Rubínový kříž', Barva.ČERVENÁ),
            ('Tyrkysová tiára', Barva.TYRKYS, 'Tyrkysovou tiáru'),
            ('Ametystový kalich', Barva.FIALOVÁ),
            ('Safírový trojzubec', Barva.MODRÁ)
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
                                 'l': JeskyněLék,
                                 'A': JeskyněArtefakt,
                                 'w': JeskyněZbraň,
                                 'x': LesZbraň,
                                 'm': LesLék,
                                 'M': JeskyněObchod,  # mastičkář
                                 'W': JeskyněObchod,  # zbrojíř
                                 ' ': None}[kód_místnosti]

                parametry = {}
                if kód_místnosti == 'M':
                    parametry.update(obchodník=postavy.Obchodník.mastičkář())
                elif kód_místnosti == 'W':
                    parametry.update(obchodník=postavy.Obchodník.zbrojíř())
                elif kód_místnosti == 'C':
                    parametry.update(
                        nepřítel=nepratele.náhodný_jeskynní_nepřítel()
                    )
                elif kód_místnosti == 'F':
                    parametry.update(
                        nepřítel=nepratele.náhodný_lesní_nepřítel()
                    )
                elif kód_místnosti == 't':
                    parametry.update(nepřítel=nepratele.Netvor.lesní_troll())
                elif kód_místnosti == 'T':
                    parametry.update(nepřítel=nepratele.Netvor.troll())
                elif kód_místnosti == 'H':
                    parametry.update(nepřítel=nepratele.Člověk.dobrodruh())
                elif kód_místnosti == 'A':
                    parametry.update(
                        artefakt=veci.Artefakt(*data_artefaktů.pop())
                    )
                elif kód_místnosti in ('w', 'x'):
                    parametry.update(zbraň=next(zbraně_iterátor))
                elif kód_místnosti in ('m', 'l'):
                    parametry.update(lék=next(léky_iterátor))

                if typ_místnosti:
                    místnost = typ_místnosti(x, y, **parametry)
                    řádka_mapy.append(místnost)
                    if kód_místnosti == 'S':
                        místnost.text = (
                            'Stojíš při okraji tajuplného lesa na úpatí'
                            ' nehostinné Hory běsů. Vrchol jejího hrozivého'
                            ' štítu je zahalen nízkým mračnem.'
                        )
                        já.začátek = místnost
                else:
                    řádka_mapy.append(None)

            já.mapa.append(řádka_mapy)

    def poklad_posbírán(já):
        return all(místnost.artefakt_sebrán for místnost in já
                   if hasattr(místnost, 'artefakt_sebrán'))

    def nepřátelé_pobiti(já):
        return not any(místnost.nepřítel.žije() for místnost in já
                       if hasattr(místnost, 'nepřítel'))

    def vše_navštíveno(já):
        return all(místnost.navštívena for místnost in já)

    def mapa_navštívených(já, pozice_hráče):
        mapa = []
        ořez_vlevo, ořez_vpravo = 1000, 1000
        for řádka in já.mapa:
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
                prázdno_vlevo, prázdno_vpravo = okraje(''.join(řádka_mapy), ' ')
                ořez_vlevo = min(ořez_vlevo, prázdno_vlevo)
                ořez_vpravo = min(ořez_vpravo, prázdno_vpravo)
                mapa.append(řádka_mapy)

        for řádka_mapy in mapa:
            řádka_mapy[:ořez_vlevo] = []
            řádka_mapy[len(řádka_mapy) - ořez_vpravo:] = []

        return mapa

    def __iter__(já):
        return iter(místnost for řádka in já.mapa for místnost in řádka
                    if místnost is not None)
