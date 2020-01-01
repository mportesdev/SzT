# coding: utf-8

import random

import enemies
import items
import npc
from utils import nice_print


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError('Create a subclass instead!')

    def modify_player(self, player):
        pass


class PlainTile(MapTile):
    def intro_text(self):
        return 'Jdeš tmavou, vlhkou a studenou jeskyní.'


class StartTile(MapTile):
    def intro_text(self):
        return ('Stojíš v tmavé jeskyni. Na stěně poblikává dohasínající'
                ' pochodeň. V šeru lze rozeznat tři cesty vedoucí ven, všechny'
                ' stejně temné a hrozivé.')


class VictoryTile(MapTile):
    def intro_text(self):
        return ('V dáli vidíš jasné světlo... snažíš se k němu přiblížit...'
                ' záře postupně sílí... je to slunce!')


class EnemyTile(MapTile):
    def __init__(self, x, y):
        enemy_class, kwargs = random.choices(enemies.enemies_data,
                                             cum_weights=[4, 7, 9, 10, 10.5],
                                             k=1)[0]
        self.enemy = enemy_class(**kwargs)
        super().__init__(x, y)

    def intro_text(self):
        return self.enemy.text

    def modify_player(self, player):
        if self.enemy.is_alive():
            player.hp = max(0, player.hp - self.enemy.damage)
            message = f'{self.enemy} útočí. '
            if player.hp > 0:
                message += f'Zbývá ti {player.hp} % zdraví.'
            else:
                message += 'Jsi mrtev!\n'
            nice_print(message, 'fight', color='91')
        else:
            try:
                if not self.enemy.gold_claimed and self.enemy.gold > 0:
                    self.enemy.gold_claimed = True
                    player.gold += self.enemy.gold
                    message = (f'Sebral jsi {self.enemy.name_dative.lower()}'
                               f' {self.enemy.gold} zlaťáků.')
                    nice_print(message, 'luck')
                if not self.enemy.weapon_claimed:
                    self.enemy.weapon_claimed = True
                    player.inventory.append(self.enemy.weapon)
                    message = (f'Sebral jsi {self.enemy.name_dative.lower()}'
                               f' {self.enemy.weapon.name_accusative.lower()}.')
                    nice_print(message, 'luck')
            except AttributeError:
                pass


class TraderTile(MapTile):
    def __init__(self, x, y):
        self.trader = npc.Trader()
        super().__init__(x, y)

    def trade(self, buyer, seller):
        valid_choices = set()
        for i, item in enumerate(seller.inventory, 1):
            if item.value <= buyer.gold:
                valid_choices.add(i)
                item_number = f'{i:3}.'
            else:
                item_number = '    '
            print(f'{item_number} {item.name} - {item.value} zlaťáků')

        while True:
            user_input = input('Č. položky nebo (Z)pět: ').upper()
            if user_input == 'Z':
                return
            else:
                try:
                    choice = int(user_input)
                    if choice not in valid_choices:
                        raise ValueError
                    to_swap = seller.inventory[choice - 1]
                    self.swap(seller, buyer, to_swap)
                    return
                except ValueError:
                    print('Neplatná volba.')

    @staticmethod
    def swap(seller, buyer, item):
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
                print('Obchodník nabízí tyto věci:')
                self.trade(buyer=player, seller=self.trader)
            elif user_input in ['P', 'p']:
                print('Tyto věci můžeš prodat:')
                self.trade(buyer=self.trader, seller=player)
            else:
                print('Neplatná volba.')

    def intro_text(self):
        return ('Malý podivný tvor sedí v koutě a cinká zlatými mincemi. Zdá'
                ' se, že by byl ochoten něco prodat nebo koupit.')


class FindGoldTile(PlainTile):
    def __init__(self, x, y):
        self.gold = random.randint(5, 50)
        self.gold_claimed = False
        super().__init__(x, y)

    def modify_player(self, player):
        if not self.gold_claimed:
            self.gold_claimed = True
            player.gold += self.gold
            message = f'Našel jsi {self.gold} zlaťáků.'
            nice_print(message, 'luck')


class FindWeaponTile(PlainTile):
    def __init__(self, x, y):
        self.weapon = random.choice((items.ColdWeapon('Kámen', 5, 1),
                                     items.ColdWeapon('Dýka', 10, 20, 'Dýku'),
                                     items.ColdWeapon('Rezavý meč', 20, 100)))
        self.weapon_claimed = False
        super().__init__(x, y)

    def modify_player(self, player):
        if not self.weapon_claimed:
            self.weapon_claimed = True
            player.inventory.append(self.weapon)
            message = f'Našel jsi {self.weapon.name_accusative.lower()}.'
            nice_print(message, 'luck')


world_dsl = """
|VT|EN|FW|EN|  |  |EN|  |  |  |  |FG|
|  |  |  |PT|FG|  |PT|  |FW|  |PT|EN|
|  |  |  |  |PT|  |PT|  |EN|  |EN|  |
|  |TT|  |  |EN|EN|PT|EN|PT|  |PT|EN|
|EN|PT|EN|FW|PT|  |  |  |PT|  |PT|  |
|  |PT|  |  |EN|PT|PT|  |PT|PT|TT|PT|
|EN|PT|FG|  |PT|  |ST|PT|EN|  |PT|  |
|  |  |PT|EN|PT|  |PT|  |FG|  |EN|EN|
|  |  |  |  |  |  |FG|  |  |  |FW|  |
"""

world_map = []

start_tile_location = []


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


def parse_world_dsl():
    if not is_dsl_valid(world_dsl):
        raise SyntaxError('DSL is invalid!')

    dsl_lines = world_dsl.strip().splitlines()

    for y, dsl_row in enumerate(dsl_lines):
        row = []
        dsl_cells = dsl_row.strip('|').split('|')
        for x, dsl_cell in enumerate(dsl_cells):
            tile_type = {'VT': VictoryTile,
                         'PT': PlainTile,
                         'EN': EnemyTile,
                         'ST': StartTile,
                         'FG': FindGoldTile,
                         'FW': FindWeaponTile,
                         'TT': TraderTile,
                         '  ': None}[dsl_cell]

            if tile_type == StartTile:
                start_tile_location[:] = x, y
            row.append(tile_type(x, y) if tile_type else None)

        world_map.append(row)
