# coding: utf-8

import math
import random

from . import agent, data, nepratele, postavy, veci, vypocty


class Místnost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.navštívena = False
        self.viděna = False
        self.text = None

    def dopad_na_hráče(self, hráč):
        pass

    def popis(self):
        return self.text


class Jeskyně(Místnost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.text = data.texty_jeskyně[self.zóna()]

    def zóna(self):
        vzdálenost_od_středu = math.hypot(self.x - 18, self.y - 10)
        return min(int(vzdálenost_od_středu / 3), 5)


class Les(Místnost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.text = data.texty_les[self.zóna()]

    def zóna(self):
        vzdálenost_od_středu = math.hypot(self.x - 18, self.y - 10)
        return int(vzdálenost_od_středu / 3) // 2


class MístnostBojMixin:
    def __init__(self, *args, nepřítel):
        super().__init__(*args)
        self.nepřítel = nepřítel

    def popis(self):
        return self.text + ' ' + self.nepřítel.text

    def dopad_na_hráče(self, hráč):
        if self.nepřítel.žije():
            if hráč.zdařilý_zásah:
                agent.zpráva_zdařilý_zásah(self.nepřítel)
            else:
                skutečný_zásah_nepřítele = vypocty.s_odchylkou(self.nepřítel.útok)
                obranný_bonus = min(hráč.zkušenost // 200, 5)
                skutečný_zásah = min(skutečný_zásah_nepřítele - obranný_bonus,
                                     hráč.zdraví)
                hráč.zdraví -= max(skutečný_zásah, 0)
                if hráč.žije():
                    hráč.zkušenost += 1
                agent.zpráva_o_zranění(hráč, self.nepřítel, skutečný_zásah)
        else:
            try:
                if not self.nepřítel.zlato_sebráno and self.nepřítel.zlato > 0:
                    self.nepřítel.zlato_sebráno = True
                    hráč.zlato += self.nepřítel.zlato
                    agent.zpráva_kořist_zlato(self.nepřítel)
                if not self.nepřítel.zbraň_sebrána:
                    self.nepřítel.zbraň_sebrána = True
                    hráč.inventář.append(self.nepřítel.zbraň)
                    agent.zpráva_kořist_zbraň(self.nepřítel)
            except AttributeError:
                pass


class MístnostObchodMixin:
    def __init__(self, *args, obchodník):
        super().__init__(*args)
        self.text = 'Stojíš u vchodu do jeskyně.'
        self.obchodník = obchodník

    def proveď_obchod(self, kupující, prodejce):
        věci_na_prodej = [věc for věc in prodejce.inventář
                          if věc.cena is not None]
        if not věci_na_prodej:
            agent.piš(
                f'{prodejce.jméno} už nemá co nabídnout.'
                if prodejce is self.obchodník
                else 'Nemáš nic, co bys mohl prodat.'
            )
            return

        agent.piš(
            f'{prodejce.jméno} nabízí tyto věci:'
            if prodejce is self.obchodník
            else 'Tyto věci můžeš prodat:'
        )

        možnosti = set()
        for číslo, věc in enumerate(věci_na_prodej, 1):
            cena = (kupující.výkupní_cena(věc) if kupující is self.obchodník
                    else věc.cena)
            if cena <= kupující.zlato:
                možnosti.add(číslo)
                číslo_položky = číslo
            else:
                číslo_položky = None
            agent.vypiš_věc_v_obchodě(číslo_položky, věc, cena)

        try:
            název_peněz, oslovení = kupující.mluva
        except AttributeError:
            název_peněz, oslovení = prodejce.mluva

        if not možnosti:
            agent.piš(
                f'"Došly mi {název_peněz}, {oslovení}!" říká '
                f'{kupující.jméno.lower()}.'
                if kupující is self.obchodník
                else 'Na žádnou z nich nemáš peníze.'
            )
            return

        vstup = agent.vstup_číslo_položky(možnosti | {''})
        if vstup == '':
            return

        vybraná_věc = prodejce.inventář[vstup - 1]
        if prodejce is self.obchodník:
            kupující.kup(vybraná_věc, prodejce)
        else:
            prodejce.prodej(vybraná_věc, kupující)
        agent.piš(
            f'"Bylo mi potěšením, {oslovení}." říká '
            f'{self.obchodník.jméno.lower()}.'
        )

    def obchoduj(self, hráč):
        while True:
            vstup = agent.vstup_koupit_prodat()
            if vstup == '':
                return

            if vstup == 'K':
                kupující, prodejce = hráč, self.obchodník
            else:
                kupující, prodejce = self.obchodník, hráč
            self.proveď_obchod(kupující=kupující, prodejce=prodejce)

    def popis(self):
        return self.text + ' ' + self.obchodník.text


class MístnostZlatoMixin:
    def __init__(self, *args):
        super().__init__(*args)
        self.zlato = random.randint(12, 24)
        self.zlato_sebráno = False

    def dopad_na_hráče(self, hráč):
        if not self.zlato_sebráno:
            self.zlato_sebráno = True
            hráč.zlato += self.zlato
            agent.vypiš_odstavec(f'Našel jsi {self.zlato} zlaťáků.', 'štěstí')


class MístnostArtefaktMixin:
    def __init__(self, *args, artefakt):
        super().__init__(*args)
        self.artefakt = artefakt
        self.artefakt_sebrán = False

    def dopad_na_hráče(self, hráč):
        if not self.artefakt_sebrán:
            self.artefakt_sebrán = True
            hráč.artefakty.append(self.artefakt)
            agent.vypiš_odstavec(
                f'Našel jsi {self.artefakt.název_4_pád.lower()}.',
                'štěstí'
            )
            if hráč.svět.poklad_posbírán():
                odměna = 300
                hráč.zkušenost += odměna
                agent.zpráva_o_odměně('nalezení všech magických předmětů',
                                      odměna)
                agent.vypiš_odstavec('Artefakty teď musíš vynést ven z'
                                     ' jeskyně a dojít s nimi na začátek své'
                                     ' cesty.')

                # vytvořit dodatečné nepřátele
                jeskyně_boj = JeskyněBoj(22, 12,
                                         nepřítel=nepratele.Netvor.troll())
                jeskyně_boj.viděna = True
                jeskyně_boj.navštívena = True
                hráč.svět[22, 12] = jeskyně_boj

                les_boj = LesBoj(27, 18,
                                 nepřítel=nepratele.Netvor.lesní_troll())
                les_boj.viděna = True
                les_boj.navštívena = True
                hráč.svět[27, 18] = les_boj


class MístnostZbraňMixin:
    def __init__(self, *args, zbraň):
        super().__init__(*args)
        self.zbraň = zbraň
        self.zbraň_sebrána = False

    def dopad_na_hráče(self, hráč):
        if not self.zbraň_sebrána:
            self.zbraň_sebrána = True
            hráč.inventář.append(self.zbraň)
            if isinstance(self, Les):
                zpráva = ('V křoví u cesty jsi našel'
                          f' {self.zbraň.název_4_pád.lower()}.')
            else:
                zpráva = ('Ve skulině pod kamenem jsi našel'
                          f' {self.zbraň.název_4_pád.lower()}.')
            agent.vypiš_odstavec(zpráva, 'štěstí')


class MístnostLékMixin:
    def __init__(self, *args, lék):
        super().__init__(*args)
        self.lék = lék
        self.lék_sebrán = False

    def dopad_na_hráče(self, hráč):
        if not self.lék_sebrán:
            self.lék_sebrán = True
            hráč.inventář.append(self.lék)
            if isinstance(self, Les):
                zpráva = f'Našel jsi {self.lék.název_4_pád.lower()}.'
            else:
                zpráva = ('Na zemi jsi našel zaprášenou'
                          f' {self.lék.název_4_pád.lower()}.')
            agent.vypiš_odstavec(zpráva, 'štěstí')


class JeskyněBoj(MístnostBojMixin, Jeskyně): ...


class LesBoj(MístnostBojMixin, Les): ...


class JeskyněObchod(MístnostObchodMixin, Jeskyně): ...


class JeskyněZlato(MístnostZlatoMixin, Jeskyně): ...


class JeskyněArtefakt(MístnostArtefaktMixin, Jeskyně): ...


class JeskyněZbraň(MístnostZbraňMixin, Jeskyně): ...


class LesZbraň(MístnostZbraňMixin, Les): ...


class JeskyněLék(MístnostLékMixin, Jeskyně): ...


class LesLék(MístnostLékMixin, Les): ...


class Svět:
    def __init__(self):
        self.mapa = []
        self.začátek = None
        self.pozice_začátku = None
        self.načti_mapu(data.řádky_mapy)

    def načti_mapu(self, řádky_mapy):

        def generátor_zbraní():
            data_zbraní = set(data.data_zbraní)

            while True:
                if (x, y) == (27, 23):
                    yield veci.Zbraň('Rezavá dýka', 9, 31, 'Rezavou dýku')
                elif (x, y) == (15, 18):
                    yield veci.Zbraň('Zrezivělý meč', 14, 68)
                elif (x, y) == (35, 14):
                    yield veci.Zbraň('Těžká sekera', 26, 117, 'Těžkou sekeru')
                else:
                    yield veci.Zbraň(*data_zbraní.pop())

        def generátor_léků():
            data_léků = set(data.data_léků)

            while True:
                if (x, y) == (34, 23):
                    yield veci.Lék('Léčivé bylinky', 18, 19,
                                   'Léčivými bylinkami')
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
        data_artefaktů = set(data.data_artefaktů)

        for y, řádka in enumerate(řádky_mapy):
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
                            ' nehostinné, v širém okolí obávané Hory běsů.'
                            ' Vrchol jejího hrozivého štítu je zahalen nízkým'
                            ' mračnem.'
                        )
                        self.začátek = místnost
                        self.pozice_začátku = x, y
                else:
                    řádka_mapy.append(None)

            self.mapa.append(řádka_mapy)

    def poklad_posbírán(self):
        return all(místnost.artefakt_sebrán for místnost in self
                   if hasattr(místnost, 'artefakt_sebrán'))

    def nepřátelé_pobiti(self):
        # vrátit True až po zabití dodatečných nepřátel
        if not self.poklad_posbírán():
            return False

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
                    if místnost is self[pozice_hráče]:
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
                prázdno_vlevo, prázdno_vpravo = vypocty.okraje(
                    ''.join(řádka_mapy),
                    ' '
                )
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

    def __getitem__(self, pozice):
        x, y = pozice

        if x < 0 or y < 0:
            return None

        try:
            return self.mapa[y][x]
        except IndexError:
            return None

    def __setitem__(self, pozice, místnost):
        x, y = pozice
        self.mapa[y][x] = místnost
