# coding: utf-8

import random

import enemies
import items
import npc


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError('Create a subclass instead!')

    def modify_player(self, player):
        pass


class StartTile(MapTile):
    def intro_text(self):
        return ('Nacházíš se v jeskyni s poblikávající pochodní na stěně.'
                ' V šeru lze rozeznat tři cesty vedoucí ven, všechny stejně'
                ' temné a hrozivé.')


class VictoryTile(MapTile):
    def modify_player(self, player):
        player.victory = True

    def intro_text(self):
        return ('V dáli vidíš jasné světlo...\n'
                '... jak se přibližuješ, postupně sílí! Je to sluneční'
                ' svit!\n\n\n'
                'Dokázal jsi to!')


class EnemyTile(MapTile):
    def __init__(self, x, y):
        r = random.random()
        if r < 0.40:
            self.enemy = enemies.Animal('Obří pavouk', 12, 6,
                                        'Pavoukovi', 'Pavouka')
            self.alive_text = ('Obří pavouk seskočil ze své sítě přímo před'
                               ' tebe!')
            self.dead_text = 'Na zemi leží tlející mrtvola pavouka.'
        elif r < 0.70:
            self.enemy = enemies.Monster('Zlobr', 32, 12, 'Zlobrovi', 'Zlobra')
            self.alive_text = 'Cestu ti zastoupil zlobr!'
            self.dead_text = 'Zde leží mrtvý zlobr, kterého jsi sám zdolal.'
        elif r < 0.90:
            self.enemy = enemies.Animal('Kolonie netopýrů', 98, 4,
                                        'Netopýrům', 'Netopýry')
            self.alive_text = ('Slyšíš postupně sílící pištivý zvuk'
                               '... náhle jsi uprostřed hejna netopýrů!')
            self.dead_text = 'Kolem se povalují desítky mrtvých netopýrů.'
        else:
            self.enemy = enemies.Monster('Kamenný obr', 82, 16,
                                         'Obrovi', 'Obra')
            self.alive_text = 'Vyrušil jsi dřímajícího kamenného obra!'
            self.dead_text = ('Přemožený obr se proměnil nazpět v obyčejnou'
                              ' skálu.')

        super().__init__(x, y)

    def intro_text(self):
        text = self.alive_text if self.enemy.is_alive() else self.dead_text
        return text

    def modify_player(self, player):
        if self.enemy.is_alive():
            player.hp = max(0, player.hp - self.enemy.damage)
            print(f'Utrpěl jsi zranění za {self.enemy.damage}.'
                  f' Zbývá ti {player.hp} % zdraví.')


class TraderTile(MapTile):
    def __init__(self, x, y):
        self.trader = npc.Trader()
        super().__init__(x, y)

    def trade(self, buyer, seller):
        for i, item in enumerate(seller.inventory, 1):
            print(f'{i}. {item.name} - {item.value} zlaťáků')
        while True:
            user_input = input('Č. položky nebo (Z)pět: ').upper()
            if user_input == 'Z':
                return
            else:
                try:
                    choice = int(user_input)
                    if choice < 1:
                        raise IndexError
                    to_swap = seller.inventory[choice - 1]
                    self.swap(seller, buyer, to_swap)
                    return
                except (ValueError, IndexError):
                    print('Neplatná volba.')

    @staticmethod
    def swap(seller, buyer, item):
        if item.value > buyer.gold:
            print('Na to nemáš peníze!')
            return
        seller.inventory.remove(item)
        buyer.inventory.append(item)
        seller.gold += item.value
        buyer.gold -= item.value
        print('Obchod uzavřen!')

    def check_if_trade(self, player):
        while True:
            user_input = input('(K)oupit, (P)rodat nebo (Z)pět? ').upper()
            if user_input == 'Z':
                return
            elif user_input in ['K', 'k']:
                print('Tyto věci můžeš koupit:')
                self.trade(buyer=player, seller=self.trader)
            elif user_input in ['P', 'p']:
                print('Tyto věci můžeš prodat:')
                self.trade(buyer=self.trader, seller=player)
            else:
                print('Neplatná volba.')

    def intro_text(self):
        return ('Malý podivný tvor sedí v koutě a cinká zlatými mincemi. Zdá'
                ' se, že by byl ochoten něco prodat nebo koupit.')


class FindGoldTile(MapTile):
    def __init__(self, x, y):
        self.gold = random.randint(5, 50)
        self.gold_claimed = False
        super().__init__(x, y)

    def modify_player(self, player):
        if not self.gold_claimed:
            self.gold_claimed = True
            player.gold += self.gold
            print(f'Našel jsi {self.gold} zlaťáků.')

    def intro_text(self):
        return 'Další nezajímavá část jeskyně. Musíš postupovat dál.'


class FindWeaponTile(MapTile):
    def __init__(self, x, y):
        self.weapon = random.choice((items.Rock,
                                     items.Dagger,
                                     items.RustySword))()
        self.weapon_claimed = False
        super().__init__(x, y)

    def modify_player(self, player):
        if not self.weapon_claimed:
            self.weapon_claimed = True
            player.inventory.append(self.weapon)
            print(f'Našel jsi {self.weapon.name.lower()}.')

    def intro_text(self):
        return 'Další nezajímavá část jeskyně. Musíš postupovat dál.'


world_dsl = """
|EN|EN|VT|EN|EN|
|EN|  |  |  |FW|
|EN|FG|EN|  |TT|
|TT|  |ST|FG|EN|
|FG|  |EN|  |FG|
"""

world_map = []

start_tile_location = None


def tile_at(x, y):
    if x < 0 or y < 0:
        return None

    try:
        return world_map[y][x]
    except IndexError:
        return None


def is_dsl_valid(dsl):
    if dsl.count('|ST|') != 1:
        return False
    if '|VT|' not in dsl:
        return False
    lines = dsl.strip().splitlines()
    pipe_counts = [line.count('|') for line in lines]
    for count in pipe_counts:
        if count != pipe_counts[0]:
            return False

    return True


tile_type_dict = {'VT': VictoryTile,
                  'EN': EnemyTile,
                  'ST': StartTile,
                  'FG': FindGoldTile,
                  'FW': FindWeaponTile,
                  'TT': TraderTile,
                  '  ': None}


def parse_world_dsl():
    if not is_dsl_valid(world_dsl):
        raise SyntaxError('DSL is invalid!')

    dsl_lines = world_dsl.strip().splitlines()

    for y, dsl_row in enumerate(dsl_lines):
        row = []
        dsl_cells = dsl_row.strip('|').split('|')
        for x, dsl_cell in enumerate(dsl_cells):
            tile_type = tile_type_dict[dsl_cell]
            if tile_type == StartTile:
                global start_tile_location
                start_tile_location = x, y
            row.append(tile_type(x, y) if tile_type else None)

        world_map.append(row)
