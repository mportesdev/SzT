# coding: utf-8


class Enemy:
    def __init__(self):
        raise NotImplementedError('Do not create raw Enemy objects.')

    def __str__(self):
        return self.name

    def is_alive(self):
        return self.hp > 0


class Animal(Enemy):
    def __init__(self, name, hp, damage,
                 name_dative=None, name_accusative=None):
        self.name = name
        self.hp = hp
        self.damage = damage

        self.name_dative = name_dative or self.name
        self.name_accusative = name_accusative or self.name


class Monster(Enemy):
    def __init__(self, name, hp, damage,
                 name_dative=None, name_accusative=None):
        self.name = name
        self.hp = hp
        self.damage = damage

        self.name_dative = name_dative or self.name
        self.name_accusative = name_accusative or self.name
