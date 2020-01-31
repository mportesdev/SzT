# coding: utf-8

from typing import List, Union

import items
from utils import BLUE, MAGENTA, CYAN, \
                  color_print, nice_print, award_bonus, oscillate
from world import World

InventoryList = List[Union[items.Weapon, items.Consumable]]


class Player:
    def __init__(self):
        self.inventory: InventoryList = [
            items.Weapon('Tupý nůž', 5, 14),
            items.Consumable('Bylinkový chleba', 8, 11, 'Bylinkovým chlebem'),
        ]
        self.gemstones = []
        self.world = World()
        self.x, self.y = self.world.start_tile.x, self.world.start_tile.y
        self.hp = 100
        self.gold = 10
        self.xp = 0
        self.good_hit = False

    def is_alive(self):
        return self.hp > 0

    def print_inventory(self):
        print('Máš u sebe:')
        for item in self.inventory:
            print(f'            {item}')
        for gemstone in self.gemstones:
            color_print(f'            < {gemstone} >', color=gemstone.color)

    def best_weapon(self):
        try:
            return max((item for item in self.inventory
                        if hasattr(item, 'damage')),
                       key=lambda weapon: weapon.damage)
        except ValueError:
            return

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_west(self):
        self.move(dx=-1, dy=0)

    def attack(self):
        enemy = self.current_room().enemy
        best_weapon = self.best_weapon()
        if best_weapon:
            weapon_damage = best_weapon.damage
            weapon_name = best_weapon.name_4.lower()
        else:
            weapon_damage = 1
            weapon_name = 'pěsti'
        real_weapon_damage = oscillate(weapon_damage)
        self.good_hit = (real_weapon_damage > weapon_damage * 1.1
                         and enemy.name_short not in ('troll', 'dobrodruh'))
        attack_bonus = self.xp // 100
        real_damage = min(real_weapon_damage + attack_bonus, enemy.hp)
        enemy.hp -= real_damage
        self.xp += real_damage
        message = (f'Použil jsi {weapon_name} proti'
                   f' {enemy.name_3.lower()}.')
        if not enemy.is_alive():
            message += f' Zabil jsi {enemy.name_4.lower()}!'
        nice_print(message, 'fight')
        if self.world.all_enemies_dead():
            award_bonus(self, 200, 'zabití všech nepřátel')

    def has_consumables(self):
        return any(isinstance(item, items.Consumable)
                   for item in self.inventory)

    def heal(self):
        consumables = [item for item in self.inventory
                       if isinstance(item, items.Consumable)]

        print('Čím se chceš kurýrovat?')
        for i, item in enumerate(consumables, 1):
            print(f'{i:3}. ', end='')
            color_print(f'{item.str_7()}', color=CYAN)

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
                    if choice < 1:
                        raise IndexError
                    to_eat = consumables[choice - 1]
                    self.hp = min(100, self.hp + to_eat.healing_value)
                    self.inventory.remove(to_eat)
                    print('Hned je ti lépe!')
                    return
                except (ValueError, IndexError):
                    color_print('?', color=MAGENTA)

    def trade(self):
        self.current_room().facilitate_trade(self)

    def current_room(self):
        return self.world.tile_at(self.x, self.y)

    def is_winner(self):
        return self.current_room() is self.world.start_tile \
               and self.world.treasure_collected()

    def print_map(self):
        map_data = self.world.map_of_visited((self.x, self.y))

        print('\n'.join(''.join(row_data)
                        for row_data in map_data))
        color_print('[ + les           # jeskyně         H hráč    ]',
                    color=BLUE)
