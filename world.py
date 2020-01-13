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
        self.text = random.choice(('Jsi v chladné tmavé jeskyni.',
                                   'Stojíš v nízké, vlhké části jeskyně.',
                                   'Procházíš úzkou podzemní chodbou.'))


class Forest(PlainTile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.text = random.choice(('Stojíš v pološeru hustého prastarého lesa.',
                                   'Jdeš po zarostlé lesní pěšině.',
                                   'Ztěžka překračuješ kořeny a padlé kmeny'
                                   ' stromů.'))


class StartTile(Forest):
    def intro_text(self):
        return ('Stojíš na úpatí kopce na okraji tajuplného lesa. Svou rodnou'
                ' vesnici jsi nechal za sebou a vydal ses na nejistou dráhu'
                ' dobrodruha.')


class VictoryTile(Cave):
    def intro_text(self):
        return self.text + ('.. v šeru kolem tebe se třpytí nesmírné množství'
                            ' blyštivých kamínků... objevil jsi podzemní'
                            ' diamantový poklad obrovské ceny!')


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
            print('Obchodník už nemá co nabídnout.' if seller is self.trader
                  else 'Nemáš nic, co bys mohl prodat.')
            return
        else:
            print('Obchodník nabízí tyto věci:' if seller is self.trader
                  else 'Tyto věci můžeš prodat:')

        valid_choices = set()
        for i, item in enumerate(seller.inventory, 1):
            if item.value <= buyer.gold:
                valid_choices.add(i)
                item_number = f'{i:3}.'
            else:
                item_number = '    '
            print(f'{item_number} ', end='')
            color_print(f'{item} '.ljust(WIDTH - 25, '.')
                        + f' {item.value:3} zlaťáků', color='96')

        try:
            money, title = buyer.slang
        except AttributeError:
            money, title = seller.slang

        if not valid_choices:
            print(f'"Došly mi {money}, {title}!" říká obchodník.'
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
                    seller.gold += to_swap.value
                    buyer.gold -= to_swap.value
                    print(f'"Bylo mi potěšením, {title}!" říká obchodník.')
                    return
                except ValueError:
                    color_print('?', color='95')

    def check_if_trade(self, player):
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
  VHTwC  C    g
m     cg c w cC
fmfffm c c CcC 
f f f  CCcCc cC
 fm WcCc     c 
mf Cc  c m ffMc
f   c  C fxf c 
fm Ccg c f m CC
f wc cCc f F g 
 g c     S     
 c T   g       
cCccgCcc       
 g g   cg      
'''

_world_repr = '''
 m                                 
 fff      ccc                      
  f      ccccc                     
  f      cccccc    c               
 ff  f        cHcc c c             
 f  fff       c  cccccc     cccc   
 ff f f       c      T    ccccw    
f fff m f     c      cccccccc      
f f m fff   c          c  c        
fmf     fW  c  w      ccccc        
f ff     cccc  c    ccc            
ff f        cccc  ccc c     g      
 f m     gccc  cccc   c   ccc  cw  
mf        c cgcc  c   ccccc ccccc  
 ff      cc              g    cc   
         c        f     cc         
         T    ffm f     c          
         cg   f  ffff   M          
         c    ffff f    f          
       cccccg  f   f mf f ffff m   
    cccg  c       mf  fff  f fff   
    gccc cccc      fff  ffff   f   
    ccgc g ccccc     f  f  m fff   
     ccc c ccgcg     fffff   f   f 
      cg c wcccc     m f f fffff fm
                       f f  f  fff 
                            ffm  f 
                                 f 
                                 S 
'''

world_map = []

start_tile_location = []


def tile_at(x, y):
    if x < 0 or y < 0:
        return None

    try:
        return world_map[y][x]
    except IndexError:
        return None


def validate_map_data(map_repr):
    if map_repr.count('S') != 1:
        raise SyntaxError('Map must contain exactly 1 start tile')
    if 'V' not in map_repr:
        raise SyntaxError('Missing victory tile')
    lines = map_repr.strip('\n').splitlines()
    line_lengths = [len(line) for line in lines]
    for line_length in line_lengths:
        if line_length != line_lengths[0]:
            raise SyntaxError('All map rows must have the same length')


def parse_world_repr():
    validate_map_data(world_repr)
    lines = world_repr.strip('\n').splitlines()

    for y, line in enumerate(lines):
        map_row = []
        for x, tile_code in enumerate(line):
            tile_type = {'V': VictoryTile,
                         'c': Cave,
                         'f': Forest,
                         'C': CaveWithEnemy,
                         'F': ForestWithEnemy,
                         'T': CaveWithEnemy,    # troll
                         'H': CaveWithEnemy,    # human
                         'S': StartTile,
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
            elif tile_code == 'T':
                kwargs.update(enemy=enemies.Monster.new_troll())
            elif tile_code == 'H':
                kwargs.update(enemy=enemies.Human.new_human())

            if tile_type == StartTile:
                start_tile_location[:] = x, y
            map_row.append(tile_type(x, y, **kwargs) if tile_type else None)

        world_map.append(map_row)
