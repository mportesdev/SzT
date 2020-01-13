# coding: utf-8

from typing import List, Union

import items
from utils import color_print, nice_print, oscillate

InventoryList = List[Union[items.Weapon, items.Consumable]]


class Player:
    def __init__(self, world):
        self.inventory: InventoryList = [
            items.Weapon('Nůž na chleba', 5, 14),
            items.Consumable('Bylinkový chleba', 8, 11),
        ]
        self.world = world
        self.x, self.y = self.world.start_tile.x, self.world.start_tile.y
        self.hp = 100
        self.gold = 10
        self.experience = 0
        self.good_hit = False

    def is_alive(self):
        return self.hp > 0

    def print_info(self):
        print('Máš u sebe:')
        for item in self.inventory:
            print(f'            {item}')

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
        enemy = self.world.tile_at(self.x, self.y).enemy
        best_weapon = self.best_weapon()
        if best_weapon:
            weapon_damage = best_weapon.damage
            weapon_name = best_weapon.name_accusative.lower()
        else:
            weapon_damage = 1
            weapon_name = 'pěsti'
        real_damage = min(oscillate(weapon_damage), enemy.hp)
        self.good_hit = (real_damage > weapon_damage * 1.1
                         and enemy.name_short not in ('troll', 'dobrodruh'))
        enemy.hp -= real_damage
        self.experience += real_damage
        message = (f'Použil jsi {weapon_name} proti'
                   f' {enemy.name_dative.lower()}.')
        if not enemy.is_alive():
            message += f' Zabil jsi {enemy.name_accusative.lower()}!'
            if self.world.all_dead():
                self.experience += 500
        nice_print(message, 'fight')

    def has_consumables(self):
        return any(isinstance(item, items.Consumable)
                   for item in self.inventory)

    def heal(self):
        consumables = [item for item in self.inventory
                       if isinstance(item, items.Consumable)]

        print('Čím chceš doplnit síly?')
        for i, item in enumerate(consumables, 1):
            print(f'{i:3}. ', end='')
            color_print(f'{item}', color='96')

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
                    if choice < 1:
                        raise IndexError
                    to_eat = consumables[choice - 1]
                    self.hp = min(100, self.hp + to_eat.healing_value)
                    self.inventory.remove(to_eat)
                    print(f'Hned se cítíš lépe!')
                    return
                except (ValueError, IndexError):
                    color_print('?', color='95')

    def trade(self):
        room = self.world.tile_at(self.x, self.y)
        room.check_if_trade(self)
