# coding: utf-8

from typing import List, Union

import items
from utils import color_print, nice_print
import world

InventoryList = List[Union[items.Weapon, items.Consumable]]


class Player:
    def __init__(self):
        self.inventory: InventoryList = [items.Weapon('Dýka', 10, 20, 'Dýku')]
        self.x, self.y = world.start_tile_location
        self.hp = 100
        self.gold = 10

    def is_alive(self):
        return self.hp > 0

    def print_info(self):
        color_print(f'Zdraví:     {self.hp} %', color='1;96')
        print('Máš u sebe:')
        if self.gold > 0:
            print(f'            {self.gold} zlaťáků')
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
        best_weapon = self.most_powerful_weapon()
        if best_weapon:
            weapon_damage = best_weapon.damage
            weapon_name = best_weapon.name_accusative.lower()
        else:
            weapon_damage = 1
            weapon_name = 'pěsti'
        room = world.tile_at(self.x, self.y)
        enemy = room.enemy
        enemy.hp = max(0, enemy.hp - weapon_damage)
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
            print(f'{i}. {item}')

        while True:
            user_input = input('Č. položky nebo (Z)pět: ').upper()
            if user_input == 'Z':
                return
            else:
                try:
                    choice = int(user_input)
                    if choice < 1:
                        raise IndexError
                    to_eat = consumables[choice - 1]
                    self.hp = min(100, self.hp + to_eat.healing_value)
                    self.inventory.remove(to_eat)
                    print(f'Máš teď {self.hp} % zdraví.')
                    return
                except (ValueError, IndexError):
                    print('Neplatná volba.')

    def trade(self):
        room = world.tile_at(self.x, self.y)
        room.check_if_trade(self)
