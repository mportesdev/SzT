# coding: utf-8

import random

import enemies
import items
import npc
from utils import WIDTH, color_print, nice_print, oscillate


class PlainTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def modify_player(self, player):
        pass

    def intro_text(self):
        return self.text


class Cave(PlainTile):
    def __init__(self, x, y):
        super().__init__(x, y)
        if 24 <= x <= 31 and 5 <= y <= 8:
            self.text = ('Kráčíš po rozměklé zemi ve vlhké a zatuchlé části'
                         ' jeskyně.')
        elif (9 <= x <= 13 and 1 <= y <= 3) \
                or (4 <= x <= 7 and 20 <= y <= 24) \
                or (11 <= x <= 15 and 22 <= y <= 24):
            self.text = 'Jsi v prostorné jeskyni.'
        else:
            self.text = 'Procházíš chladnou tmavou jeskyní.'


class Forest(PlainTile):
    def __init__(self, x, y):
        super().__init__(x, y)
        if 0 <= x <= 8 and 0 <= y <= 14:
            self.text = ('Jdeš po sotva znatelné stezce vedoucí tmavým a'
                         ' zlověstně tichým lesem. V pološeru zakopáváš o'
                         ' kořeny obrovských stromů.')
        elif 14 <= x <= 20 and 15 <= y <= 19:
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
                nice_print(f'Zasáhl jsi {self.enemy.name_accusative.lower()} do'
                           f' hlavy! {self.enemy.name} zmateně vrávorá.',
                           'fight', color='96')
            else:
                player.hp = max(0, player.hp - oscillate(self.enemy.damage))
                message = f'{self.enemy} útočí. '
                if player.hp > 0:
                    message += f'Utrpěl jsi zranění.'
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
                    nice_print(message, 'luck', color='96')
                if not self.enemy.weapon_claimed:
                    self.enemy.weapon_claimed = True
                    player.inventory.append(self.enemy.weapon)
                    message = (f'Sebral jsi {self.enemy.name_dative.lower()}'
                               f' {self.enemy.weapon.name_accusative.lower()}.')
                    nice_print(message, 'luck', color='96')
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
        if not seller.inventory:
            print(f'{seller.name} už nemá co nabídnout.'
                  if seller is self.trader
                  else 'Nemáš nic, co bys mohl prodat.')
            return
        else:
            print(f'{seller.name} nabízí tyto věci:' if seller is self.trader
                  else 'Tyto věci můžeš prodat:')

        valid_choices = set()
        for i, item in enumerate(seller.inventory, 1):
            price = (buyer.buy_price(item) if buyer is self.trader
                     else item.value)
            if price <= buyer.gold:
                valid_choices.add(i)
                item_number = f'{i:3}.'
            else:
                item_number = '    '
            print(f'{item_number} ', end='')
            color_print(f'{item} '.ljust(WIDTH - 25, '.')
                        + f' {price:3} zlaťáků', color='96')

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
            color_print('Číslo položky             (', end='', color='94')
            print('Enter', end='')
            color_print(' = návrat) ', end='', color='94')
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
                    color_print('?', color='95')

    def facilitate_trade(self, player):
        while True:
            print('K', end='')
            color_print(': koupit    ', end='', color='94')
            print('P', end='')
            color_print(': prodat    (', end='', color='94')
            print('Enter', end='')
            color_print(' = návrat) ', end='', color='94')
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
                color_print('?', color='95')

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
            nice_print(message, 'luck', color='96')


class FindWeaponTile(PlainTile):
    def __init__(self, x, y):
        super().__init__(x, y)
        if (x, y) == (27, 24):
            args = ('Rezavá sekerka', 9, 32, 'Rezavou sekerku')
        else:
            args = random.choice((('Rezavý meč', 16, 72),
                                  ('Ostnatý palcát', 18, 85),
                                  ('Řemdih', 20, 94)))
        self.weapon = items.Weapon(*args)
        self.weapon_claimed = False

    def modify_player(self, player):
        if not self.weapon_claimed:
            self.weapon_claimed = True
            player.inventory.append(self.weapon)
            message = f'Našel jsi {self.weapon.name_accusative.lower()}.'
            nice_print(message, 'luck', color='96')


class CaveWithWeapon(FindWeaponTile, Cave):
    pass


class ForestWithWeapon(FindWeaponTile, Forest):
    pass


class FindConsumableTile(Forest):
    def __init__(self, x, y):
        super().__init__(x, y)
        args = random.choice((('Léčivé bylinky', 18, 20),
                              ('Kouzelné houby', 22, 26),
                              ('Kouzelné bobule', 14, 14)))
        self.consumable = items.Consumable(*args)
        self.consumable_claimed = False

    def modify_player(self, player):
        if not self.consumable_claimed:
            self.consumable_claimed = True
            player.inventory.append(self.consumable)
            message = f'Našel jsi {self.consumable.name_accusative.lower()}.'
            nice_print(message, 'luck', color='96')


world_repr = '''
 m                                 
 fff      ccc                      
  f      ccccc                     
  f      cccccc    c               
 ff  f        cHcc c c  cg         
 f  fff   ccc c  cccccc c   cccc   
 ff f f   c ccc  c   T  c ccCcw    
f fff m f c   c  cc ccccccccc      
f f m fff   c          C  C        
fmf     fW  c  wcc  c ccccccc      
f ff     cccc  c  c ccc       c    
ff f        cccc  ccc C g   gcc    
 f m     gccc  cccc c c c ccc  cw  
mf        c cgcc  c c cccCc cCccc  
 ff      cc         c c  g    cc   
         c        f   g cc         
         T    ffm f     c          
         cg   f  ffff   M          
         c    ffff t    V          
       cccccg  x   f mf f ffff m   
    cccg  c       mf  fff  f fFf   
    gccc cccc      fff  fFff   f   
    ccgc g ccccc     f  f  m fff   
     ccc c ccgcg     fffff   f   f 
      cg c wcccc     m f f xffff fm
                       f f  f  fff 
                            ffm  f 
                                 f 
                                 S 
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
                                     ' tajuplného lesa. Svou rodnou vesnici jsi'
                                     ' nechal za sebou a vydal ses na nejistou'
                                     ' dráhu dobrodruha.')
                        self.start_tile = tile
                    elif tile_code == 'V':
                        self.victory_tile = tile
                else:
                    map_row.append(None)

            self.world_map.append(map_row)

    def treasure_collected(self):
        return all(getattr(tile, 'gold_claimed', True) for tile in self)

    def all_dead(self):
        return sum(tile.enemy.hp for tile in self
                   if hasattr(tile, 'enemy')) == 0

    def __iter__(self):
        return iter(tile for row in self.world_map for tile in row)
