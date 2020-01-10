# coding: utf-8

from typing import List, Union

import items
from utils import color_print, nice_print, oscillate
import world

InventoryList = List[Union[items.Weapon, items.Consumable]]


class Player:
    def __init__(self):
        self.inventory: InventoryList = [
            items.Weapon('Nůž na chleba', 5, 14),
            items.Consumable('Bylinkový chleba', 8, 11),
        ]
        self.x, self.y = world.start_tile_location
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

    def most_powerful_weapon(self) -> items.Weapon:
        max_damage = 0
        best_weapon = None
        for item in self.inventory:
            try:
                if item.damage > max_damage:
                    best_weapon = item
                    max_damage = item.damage
            except AttributeError:
                pass

        return best_weapon

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
        enemy = world.tile_at(self.x, self.y).enemy
        best_weapon = self.most_powerful_weapon()
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
        room = world.tile_at(self.x, self.y)
        room.check_if_trade(self)
