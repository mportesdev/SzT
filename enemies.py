# coding: utf-8


class Enemy:
    def __init__(self):
        raise NotImplementedError('Do not create raw Enemy objects.')

    def __str__(self):
        return self.name

    def is_alive(self):
        return self.hp > 0


class Animal(Enemy):
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage


class Monster(Enemy):
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage
