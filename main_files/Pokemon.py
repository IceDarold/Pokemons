import random
from enum import Enum
from typing import Any

import pygame
from pygame import Surface
from pygame.sprite import Sprite

from Pokemons.Base_classes.game_object import GameObject
from Pokemons.Base_classes.transform import Transform
from Pokemons.UI.base_ui.text import Text


class Pokemon(GameObject):
    max_pokemon_atk = 100
    max_pokemon_df = 10

    class PokemonType(Enum):
        fire = 0
        water = 1
        grass = 2
        electric = 3

    def __init__(self, name: str, transform: Transform, image: Surface, atk: int = None, df: int = None):
        if not atk or atk < 5:
            atk = random.randint(5, 20)
        if not df or df < 5:
            df = random.randint(5, 20)
        self._name: str = name
        self._hp: int = 100
        self._atk: int = atk
        self._df: int = df
        self.hp_text: Text = None
        super().__init__(image=image, transform=transform)

    @staticmethod
    def create_pokemon(create_object: Any):
        try:
            return Pokemon(create_object.name, create_object.transform, create_object.image, create_object.atk,
                           create_object.df)
        except AttributeError:
            return None

    def attack(self, aim):
        if self._hp == 0:
            return
        damage = self._atk - aim.get_def()
        if damage < 0:
            self.damage(-damage)
        else:
            aim.damage(damage)

    def damage(self, damage):
        if self._hp == 0:
            return
        print(self.get_name(), damage, " DAMAGE!")
        self._hp -= damage
        if self._hp < 0:
            self._hp = 0

    def get_name(self):
        return self._name

    def get_hp(self):
        return self._hp

    def get_atk(self):
        return self._atk

    def get_def(self):
        return self._df

    def __str__(self):
        return f"{self.get_name()}. hp: {self._hp}"
