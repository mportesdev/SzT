# coding: utf-8

import math
import random

from . import agent, data, nepratele, postavy, utility, veci


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
        já.text = data.texty_jeskyně[já.zóna()]

    def zóna(já):
        vzdálenost_od_středu = math.hypot(já.x - 18, já.y - 10)
        return min(int(vzdálenost_od_středu / 3), 5)


class Les(Místnost):
    def __init__(já, x, y):
        super().__init__(x, y)
        já.text = data.texty_les[já.zóna()]

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
                agent.zpráva_zdařilý_zásah(já.nepřítel)
            else:
                skutečný_zásah_nepřítele = utility.s_odchylkou(já.nepřítel.útok)
                obranný_bonus = min(hráč.zkušenost // 200, 5)
                skutečný_zásah = min(skutečný_zásah_nepřítele - obranný_bonus,
                                     hráč.zdraví)
                hráč.zdraví -= max(skutečný_zásah, 0)
                if hráč.žije():
                    hráč.zkušenost += 1
                agent.zpráva_o_zranění(hráč, já.nepřítel, skutečný_zásah)
        else:
            try:
                if not já.nepřítel.zlato_sebráno and já.nepřítel.zlato > 0:
                    já.nepřítel.zlato_sebráno = True
                    hráč.zlato += já.nepřítel.zlato
                    agent.zpráva_kořist_zlato(já.nepřítel)
                if not já.nepřítel.zbraň_sebrána:
                    já.nepřítel.zbraň_sebrána = True
                    hráč.inventář.append(já.nepřítel.zbraň)
                    agent.zpráva_kořist_zbraň(já.nepřítel)
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
            agent.piš(
                f'{prodejce.jméno} už nemá co nabídnout.'
                if prodejce is já.obchodník
                else 'Nemáš nic, co bys mohl prodat.'
            )
            return
        else:
            agent.piš(
                f'{prodejce.jméno} nabízí tyto věci:'
                if prodejce is já.obchodník
                else 'Tyto věci můžeš prodat:'
            )

        možnosti = set()
        for číslo, věc in enumerate(věci_na_prodej, 1):
            cena = (kupující.výkupní_cena(věc) if kupující is já.obchodník
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
                if kupující is já.obchodník
                else 'Na žádnou z nich nemáš peníze.'
            )
            return

        while True:
            vstup = agent.vstup_číslo_položky(možnosti | {''})
            if vstup == '':
                return
            else:
                vybraná_věc = prodejce.inventář[vstup - 1]
                if prodejce is já.obchodník:
                    kupující.kup(vybraná_věc, prodejce)
                else:
                    prodejce.prodej(vybraná_věc, kupující)
                agent.piš(
                    f'"Bylo mi potěšením, {oslovení}." říká '
                    f'{já.obchodník.jméno.lower()}.'
                )
                return

    def obchoduj(já, hráč):
        while True:
            vstup = agent.vstup_koupit_prodat()
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
            agent.vypiš_odstavec(f'Našel jsi {já.zlato} zlaťáků.', 'štěstí')


class JeskyněArtefakt(Jeskyně):
    def __init__(já, x, y, artefakt):
        super().__init__(x, y)
        já.artefakt = artefakt
        já.artefakt_sebrán = False

    def dopad_na_hráče(já, hráč):
        if not já.artefakt_sebrán:
            já.artefakt_sebrán = True
            hráč.artefakty.append(já.artefakt)
            agent.vypiš_odstavec(
                f'Našel jsi {já.artefakt.název_4_pád.lower()}.',
                'štěstí'
            )
            if hráč.svět.poklad_posbírán():
                agent.uděl_odměnu(hráč, 300, 'nalezení všech magických'
                                             ' předmětů')
                agent.vypiš_odstavec('Artefakty teď musíš vynést ven z'
                                     ' jeskyně a dojít s nimi na začátek své'
                                     ' cesty.')


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
            agent.vypiš_odstavec(zpráva, 'štěstí')


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
                zpráva = f'Našel jsi {já.lék.název_4_pád.lower()}.'
            else:
                zpráva = ('Na zemi jsi našel zaprášenou'
                          f' {já.lék.název_4_pád.lower()}.')
            agent.vypiš_odstavec(zpráva, 'štěstí')


class JeskyněLék(MístnostLék, Jeskyně):
    pass


class LesLék(MístnostLék, Les):
    pass


class Svět:
    def __init__(já):
        já.mapa = []
        já.začátek = None
        já.načti_mapu(data.řádky_mapy)

    def načti_mapu(já, řádky_mapy):

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
                prázdno_vlevo, prázdno_vpravo = utility.okraje(
                    ''.join(řádka_mapy), ' '
                )
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

    def __getitem__(self, pozice):
        x, y = pozice

        if x < 0 or y < 0:
            return

        try:
            return self.mapa[y][x]
        except IndexError:
            return

    def __setitem__(self, pozice, místnost):
        x, y = pozice
        self.mapa[y][x] = místnost
