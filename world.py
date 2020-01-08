# coding: utf-8

import random

import enemies
import items
import npc
from utils import WIDTH, nice_print, oscillate


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


class EnemyTile(Cave):
    def __init__(self, x, y):
        super().__init__(x, y)
        enemy_class, kwargs = random.choices(enemies.enemies_data,
                                             cum_weights=[3, 6, 9, 12, 14, 16,
                                                          17],
                                             k=1)[0]
        self.enemy = enemy_class(**kwargs)

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


class TraderTile(Cave):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.text = 'Stojíš u vchodu do jeskyně.'
        self.trader = npc.Trader()

    def trade(self, buyer, seller):
        valid_choices = set()
        for i, item in enumerate(seller.inventory, 1):
            if item.value <= buyer.gold:
                valid_choices.add(i)
                item_number = f'{i:3}.'
            else:
                item_number = '    '
            print(f'{item_number} {item} '.ljust(WIDTH - 20, '.')
                  + f' {item.value:3} zlaťáků')

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


class FindWeaponTile(Cave):
    def __init__(self, x, y):
        super().__init__(x, y)
        args = random.choice((('Ostnatý palcát', 21, 90),
                              ('Rezavý meč', 19, 100),
                              ('Těžká sekera', 24, 110, 'Těžkou sekeru')))
        self.weapon = items.Weapon(*args)
        self.weapon_claimed = False

    def modify_player(self, player):
        if not self.weapon_claimed:
            self.weapon_claimed = True
            player.inventory.append(self.weapon)
            message = f'Našel jsi {self.weapon.name_accusative.lower()}.'
            nice_print(message, 'luck', color='96')


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


world_dsl = """
|VT|EN|FW|EN|  |  |EN|  |  |  |  |FG|
|  |  |  |CV|FG|  |CV|  |FW|  |CV|EN|
|FC|FR|FC|  |CV|  |CV|  |EN|CV|EN|  |
|  |FR|  |  |EN|EN|CV|EN|CV|  |CV|EN|
|  |TT|CV|EN|CV|  |  |  |  |  |CV|  |
|EN|CV|  |  |CV|  |FC|  |FR|FR|TT|CV|
|  |CV|  |  |EN|  |FR|FR|FR|  |CV|  |
|EN|CV|FG|  |CV|  |FR|  |FC|  |EN|EN|
|FW|  |CV|EN|CV|  |FR|  |FR|  |FG|  |
|  |  |  |  |  |  |ST|  |  |  |  |  |
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
                         'CV': Cave,
                         'FR': Forest,
                         'EN': EnemyTile,
                         'ST': StartTile,
                         'FG': FindGoldTile,
                         'FW': FindWeaponTile,
                         'FC': FindConsumableTile,
                         'TT': TraderTile,
                         '  ': None}[dsl_cell]

            if tile_type == StartTile:
                start_tile_location[:] = x, y
            row.append(tile_type(x, y) if tile_type else None)

        world_map.append(row)
