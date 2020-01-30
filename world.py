# coding: utf-8

import random

import enemies
import items
import npc
from utils import WIDTH, RED, BLUE, MAGENTA, CYAN, color_print, nice_print, \
                  award_bonus, oscillate, leading_trailing


class PlainTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False

    def modify_player(self, player):
        pass

    def intro_text(self):
        return self.text


class Cave(PlainTile):
    def __init__(self, x, y):
        super().__init__(x, y)
        if x >= 26 and y <= 8:
            self.text = ('Kráčíš po rozměklé zemi ve vlhké a zatuchlé části'
                         ' jeskyně.')
        elif x <= 16 and y >= 17:
            self.text = 'Bloudíš spletí úzkých a nízkých podzemních chodeb.'
        else:
            self.text = 'Procházíš chladnou tmavou jeskyní.'


class Forest(PlainTile):
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


class EnemyTile(PlainTile):
    def __init__(self, x, y, enemy):
        super().__init__(x, y)
        self.enemy = enemy

    def intro_text(self):
        return self.text + ' ' + self.enemy.text

    def modify_player(self, player):
        if self.enemy.is_alive():
            if player.good_hit:
                nice_print(f'Zasáhl jsi {self.enemy.name_4.lower()} do'
                           f' hlavy! {self.enemy.name} zmateně vrávorá.',
                           'fight', color=CYAN)
            else:
                real_enemy_damage = oscillate(self.enemy.damage)
                defense_bonus = player.xp // 100
                real_damage = min(real_enemy_damage - defense_bonus, player.hp)
                player.hp -= real_damage
                message = f'{self.enemy} útočí. '
                if player.is_alive():
                    message += f'Utrpěl jsi zranění.'
                    player.xp += 1
                else:
                    message += f'{random.choice(("Ouha", "Běda"))}, jsi mrtev!'
                nice_print(message, 'fight', color=RED)
        else:
            try:
                if not self.enemy.gold_claimed and self.enemy.gold > 0:
                    self.enemy.gold_claimed = True
                    player.gold += self.enemy.gold
                    message = (f'Sebral jsi {self.enemy.name_3.lower()}'
                               f' {self.enemy.gold} zlaťáků.')
                    nice_print(message, 'luck', color=CYAN)
                if not self.enemy.weapon_claimed:
                    self.enemy.weapon_claimed = True
                    player.inventory.append(self.enemy.weapon)
                    message = (f'Sebral jsi {self.enemy.name_3.lower()}'
                               f' {self.enemy.weapon.name_4.lower()}.')
                    nice_print(message, 'luck', color=CYAN)
            except AttributeError:
                pass


class CaveWithEnemy(EnemyTile, Cave):
    pass


class ForestWithEnemy(EnemyTile, Forest):
    pass


class TraderTile(Cave):
    def __init__(self, x, y, trader):
        super().__init__(x, y)
        self.text = 'Stojíš u vchodu do jeskyně.'
        self.trader = trader

    def trade(self, buyer, seller):
        sellable_items = [item for item in seller.inventory
                          if item.value is not None]
        if not sellable_items:
            print(f'{seller.name} už nemá co nabídnout.'
                  if seller is self.trader
                  else 'Nemáš nic, co bys mohl prodat.')
            return
        else:
            print(f'{seller.name} nabízí tyto věci:' if seller is self.trader
                  else 'Tyto věci můžeš prodat:')

        valid_choices = set()
        for i, item in enumerate(sellable_items, 1):
            price = (buyer.buy_price(item) if buyer is self.trader
                     else item.value)
            if price <= buyer.gold:
                valid_choices.add(i)
                item_number = f'{i:3}.'
            else:
                item_number = '    '
            print(f'{item_number} ', end='')
            color_print(f'{item} '.ljust(WIDTH - 25, '.')
                        + f' {price:3} zlaťáků', color=CYAN)

        try:
            money, title = buyer.slang
        except AttributeError:
            money, title = seller.slang

        if not valid_choices:
            print(f'"Došly mi {money}, {title}!" říká {buyer.name.lower()}.'
                  if buyer is self.trader
                  else 'Na žádnou z nich nemáš peníze.')
            return

        while True:
            color_print('Číslo položky             (', end='', color=BLUE)
            print('Enter', end='')
            color_print(' = návrat) ', end='', color=BLUE)
            user_input = input().upper()
            if user_input == '':
                return
            else:
                try:
                    choice = int(user_input)
                    if choice not in valid_choices:
                        raise ValueError
                    to_swap = seller.inventory[choice - 1]
                    seller.inventory.remove(to_swap)
                    buyer.inventory.append(to_swap)
                    price = (buyer.buy_price(to_swap) if buyer is self.trader
                             else to_swap.value)
                    seller.gold += price
                    buyer.gold -= price
                    print(f'"Bylo mi potěšením, {title}!"'
                          f' říká {self.trader.name.lower()}.')
                    return
                except ValueError:
                    color_print('?', color=MAGENTA)

    def facilitate_trade(self, player):
        while True:
            print('K', end='')
            color_print(': koupit    ', end='', color=BLUE)
            print('P', end='')
            color_print(': prodat    (', end='', color=BLUE)
            print('Enter', end='')
            color_print(' = návrat) ', end='', color=BLUE)
            user_input = input().upper()
            if user_input == '':
                return
            elif user_input in ('K', 'P'):
                if user_input == 'K':
                    buyer, seller = player, self.trader
                else:
                    buyer, seller = self.trader, player
                self.trade(buyer=buyer, seller=seller)
            else:
                color_print('?', color=MAGENTA)

    def intro_text(self):
        return self.text + ' ' + self.trader.text


class FindGoldTile(Cave):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.gold = random.randint(5, 50)
        self.gold_claimed = False

    def modify_player(self, player):
        if not self.gold_claimed:
            self.gold_claimed = True
            player.gold += self.gold
            message = f'Našel jsi {self.gold} zlaťáků.'
            nice_print(message, 'luck', color=CYAN)


class FindGemstoneTile(Cave):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.gemstone = None
        self.gemstone_claimed = False

    def modify_player(self, player):
        if not self.gemstone_claimed:
            self.gemstone_claimed = True
            player.gemstones.append(self.gemstone)
            message = f'Našel jsi {self.gemstone.name_4.lower()}.'
            nice_print(message, 'luck', color=CYAN)
            if player.world.treasure_collected():
                award_bonus(player, 300, 'nalezení všech drahokamů')


class FindWeaponTile(PlainTile):
    def __init__(self, x, y):
        super().__init__(x, y)
        if (x, y) == (27, 23):
            args = ('Rezavá dýka', 9, 32, 'Rezavou dýku')
        elif (x, y) == (15, 18):
            args = ('Zrezivělý meč', 16, 72)
        else:
            args = random.choice((('Ostnatý palcát', 18, 85),
                                  ('Řemdih', 20, 94)))
        self.weapon = items.Weapon(*args)
        self.weapon_claimed = False

    def modify_player(self, player):
        if not self.weapon_claimed:
            self.weapon_claimed = True
            player.inventory.append(self.weapon)
            if isinstance(self, Forest):
                message = ('V křoví u cesty jsi našel'
                           f' {self.weapon.name_4.lower()}.')
            else:
                message = ('Ve skulině pod kamenem jsi našel'
                           f' {self.weapon.name_4.lower()}.')
            nice_print(message, 'luck', color=CYAN)


class CaveWithWeapon(FindWeaponTile, Cave):
    pass


class ForestWithWeapon(FindWeaponTile, Forest):
    pass


class FindConsumableTile(Forest):
    def __init__(self, x, y):
        super().__init__(x, y)
        if (x, y) == (34, 23):
            args = ('Léčivé bylinky', 18, 20, 'Léčivými bylinkami')
        elif (x, y) == (30, 25):
            args = ('Léčivé houby', 12, 10, 'Léčivými houbami')
        elif (x, y) == (31, 18):
            args = ('Léčivé bobule', 13, 12, 'Léčivými bobulemi')
        else:
            args = random.choice((('Léčivé houby', 12, 10, 'Léčivými houbami'),
                                  ('Léčivé bobule', 13, 12,
                                   'Léčivými bobulemi'),
                                  ('Léčivé bylinky', 18, 20,
                                   'Léčivými bylinkami'),
                                  ('Kouzelné houby', 22, 26,
                                   'Kouzelnými houbami'),
                                  ('Kouzelné bobule', 16, 17,
                                   'Kouzelnými bobulemi')))
        self.consumable = items.Consumable(*args)
        self.consumable_claimed = False

    def modify_player(self, player):
        if not self.consumable_claimed:
            self.consumable_claimed = True
            player.inventory.append(self.consumable)
            message = f'Našel jsi {self.consumable.name_4.lower()}.'
            nice_print(message, 'luck', color=CYAN)


world_repr = '''
fm        1c cc                          
 fff    cc c c                           
  f      cccccc    c                     
  F  f        cHcc c c  cg    c          
 ff fFf   ccc c  cccccc c    cc          
 f  f f   c ccc  c   T  c    c cc        
 ff f m f 1   c  cc cccccccccccc         
f fff fff   c          C  C              
f F m   fW  c  wcc  c ccccccc            
fmf      cccc  c  c ccc       c          
f ff        cccc  ccc C g   gcc          
ff f     gccc  cccc c c c ccc  c         
 F m      c cgcc  c c cccCc cCcccc       
mf       cc         c c  g    c  c       
 ff      c        f   g cc    cc         
         T    Ffm f     c                
         cg   f  ffff   M                
     1   c    ffff t    V           ff f 
     c cccccc  x   f mf f ffff m     ffff
    cc c  c       mf  fff  f fff  ff f  m
    c  c cccc cc   fff  fFff   F   fFff  
    cccc c  c  c1    F  f  m fff fff  ff 
   cc c  c ccc c     fffff   f   f  f f  
   c  c  c w ccc     m f f xffFf fm ffFff
   c1                  f f  f  fff  f   f
                            ffm  f fm fff
                                 f f ff f
                                 S     mf
'''


class World:
    def __init__(self):
        self.world_map = []
        self.start_tile = None
        self.victory_tile = None
        self.parse_world_repr(world_repr)

    def tile_at(self, x, y):
        if x < 0 or y < 0:
            return None
        try:
            return self.world_map[y][x]
        except IndexError:
            return None

    def parse_world_repr(self, map_repr):
        gemstone_data = {('Diamant', '0'), ('Rubín', RED), ('Tyrkys', CYAN),
                         ('Ametyst', MAGENTA), ('Safír', BLUE)}

        if map_repr.count('1') > len(gemstone_data):
            raise ValueError('Not enough gemstone data')
        if map_repr.count('S') != 1 or map_repr.count('V') != 1:
            raise ValueError('Map must contain exactly 1 start tile'
                             ' and exactly 1 victory tile')

        lines = map_repr.strip('\n').splitlines()
        for y, line in enumerate(lines):
            map_row = []
            for x, tile_code in enumerate(line):
                tile_type = {'V': Forest,
                             'c': Cave,
                             'f': Forest,
                             'C': CaveWithEnemy,
                             'F': ForestWithEnemy,
                             't': ForestWithEnemy,
                             'T': CaveWithEnemy,    # troll
                             'H': CaveWithEnemy,    # human
                             'S': PlainTile,
                             'g': FindGoldTile,
                             '1': FindGemstoneTile,
                             'w': CaveWithWeapon,
                             'x': ForestWithWeapon,
                             'm': FindConsumableTile,
                             'M': TraderTile,    # trader - medicine
                             'W': TraderTile,    # trader - weapons
                             ' ': None}[tile_code]

                kwargs = {}
                if tile_code == 'M':
                    kwargs.update(trader=npc.Trader.new_medicine_trader())
                elif tile_code == 'W':
                    kwargs.update(trader=npc.Trader.new_weapon_trader())
                elif tile_code == 'C':
                    kwargs.update(enemy=enemies.random_cave_enemy())
                elif tile_code == 'F':
                    kwargs.update(enemy=enemies.random_forest_enemy())
                elif tile_code == 't':
                    kwargs.update(enemy=enemies.Monster.new_forest_troll())
                elif tile_code == 'T':
                    kwargs.update(enemy=enemies.Monster.new_troll())
                elif tile_code == 'H':
                    kwargs.update(enemy=enemies.Human.new_human())

                if tile_type:
                    tile = tile_type(x, y, **kwargs)
                    map_row.append(tile)
                    if tile_code == 'S':
                        tile.text = ('Stojíš na úpatí kopce na okraji'
                                     ' tajuplného lesa. Svou rodnou vesnici,'
                                     ' stejně jako vcelku poklidný život'
                                     ' řeznického učedníka a spořádaného'
                                     ' křesťana, jsi nechal daleko za sebou a'
                                     ' vydal ses na nejistou dráhu dobrodruha.')
                        self.start_tile = tile
                    elif tile_code == 'V':
                        self.victory_tile = tile
                    elif tile_code == '1':
                        tile.gemstone = items.Gemstone(*gemstone_data.pop())
                else:
                    map_row.append(None)

            self.world_map.append(map_row)

    def treasure_collected(self):
        return all(tile.gemstone_claimed for tile in self
                   if hasattr(tile, 'gemstone_claimed'))

    def all_enemies_dead(self):
        return not any(tile.enemy.is_alive() for tile in self
                       if hasattr(tile, 'enemy'))

    def all_tiles_visited(self):
        return all(tile.visited for tile in self)

    def map_of_visited(self, player_position):
        map_data = []
        trim_left, trim_right = 1000, 1000
        for row in self.world_map:
            row_data = []
            for tile in row:
                try:
                    if (tile.x, tile.y) == player_position:
                        row_data.append('H')
                    elif tile.visited:
                        row_data.append('#' if isinstance(tile, Cave) else '+')
                    else:
                        row_data.append(' ')
                except AttributeError:
                    row_data.append(' ')
            if set(row_data) != {' '}:
                blank_left, blank_right = leading_trailing(''.join(row_data),
                                                           ' ')
                trim_left = min(trim_left, blank_left)
                trim_right = min(trim_right, blank_right)
                map_data.append(row_data)

        for row_data in map_data:
            row_data[:trim_left] = []
            row_data[len(row_data)-trim_right:] = []

        return map_data

    def __iter__(self):
        return iter(tile for row in self.world_map for tile in row
                    if tile is not None)
