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


world_dsl = '''
|  |  |VT|HU|TR|CW|EN|  |  |EN|  |  |  |  |FG|
|FC|  |  |  |  |  |CV|FG|  |CV|  |CW|  |CV|EN|
|FR|FC|FR|FR|FR|FC|  |CV|  |CV|  |EN|CV|EN|  |
|FR|  |FR|  |FR|  |  |EN|EN|CV|EN|CV|  |CV|EN|
|  |FR|FC|  |TW|CV|EN|CV|  |  |  |  |  |CV|  |
|FC|FR|  |EN|CV|  |  |CV|  |FC|  |FR|FR|TM|CV|
|FR|  |  |  |CV|  |  |EN|  |FR|FW|FR|  |CV|  |
|FR|FC|  |EN|CV|FG|  |CV|  |FR|  |FC|  |EN|EN|
|FR|  |CW|CV|  |CV|EN|CV|  |FR|  |FE|  |FG|  |
|  |FG|  |CV|  |  |  |  |  |ST|  |  |  |  |  |
|  |CV|  |TR|  |  |  |FG|  |  |  |  |  |  |  |
|CV|EN|CV|CV|FG|EN|CV|CV|  |  |  |  |  |  |  |
|  |FG|  |FG|  |  |  |CV|FG|  |  |  |  |  |  |
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
                         'CV': Cave,
                         'FR': Forest,
                         'EN': CaveWithEnemy,
                         'FE': ForestWithEnemy,
                         'TR': CaveWithEnemy,    # troll
                         'HU': CaveWithEnemy,    # human
                         'ST': StartTile,
                         'FG': FindGoldTile,
                         'CW': CaveWithWeapon,
                         'FW': ForestWithWeapon,
                         'FC': FindConsumableTile,
                         'TM': TraderTile,    # trader - medicine
                         'TW': TraderTile,    # trader - weapons
                         '  ': None}[dsl_cell]

            kwargs = {}
            if dsl_cell == 'TM':
                kwargs.update(trader=npc.Trader.new_medicine_trader())
            elif dsl_cell == 'TW':
                kwargs.update(trader=npc.Trader.new_weapon_trader())
            elif dsl_cell == 'EN':
                kwargs.update(enemy=enemies.random_cave_enemy())
            elif dsl_cell == 'FE':
                kwargs.update(enemy=enemies.random_forest_enemy())
            elif dsl_cell == 'TR':
                kwargs.update(enemy=enemies.Monster.new_troll())
            elif dsl_cell == 'HU':
                kwargs.update(enemy=enemies.Human.new_human())

            if tile_type == StartTile:
                start_tile_location[:] = x, y
            row.append(tile_type(x, y, **kwargs) if tile_type else None)

        world_map.append(row)
