import os
from enum import Enum, IntEnum

import pygame
import random

from pygame import Vector2

from pokemons import *


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        if x1 == x2:  # вертикальная стенка
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
        self.image.fill((255, 255, 0))


class PokemonType(IntEnum):
    fire = 1
    water = 2


# noinspection PyTypeChecker
class World:
    MAX_POKEMON_ATK = 5
    MAX_POKEMON_DF = 5

    def __init__(self, n_pok, x1, y1, x2, y2, screen_width: int, screen_height: int):
        self.n_poc = n_pok
        self.rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        self.horBorders = pygame.sprite.Group()
        self.vertBorders = pygame.sprite.Group()
        self.vertBorders.add(Border(x1, y1, x1, y2))
        self.vertBorders.add(Border(x2, y1, x2, y2))
        self.horBorders.add(Border(x1, y1, x2, y1))
        self.horBorders.add(Border(x1, y2, x2, y2))
        self.pokemons = pygame.sprite.Group()
        self.generate_pokemones(general_pokemon_height=100)
        self.bg = pygame.image.load("../images/Игровое-поле-Трава-и-земля.jpg")
        self.bg_rect = self.bg.get_rect()
        self.bg_rect.center = (screen_width // 2, screen_height // 2)
        # bg = pygame.transform.scale(bg, (0.9, 0.9))
        self.bg = pygame.transform.scale(self.bg, (self.rect.width, self.rect.height))

    @staticmethod
    def get_pokemon_image(pokemon_type: PokemonType):
        pokemon_image_path = random.choice(os.listdir(f"images/{pokemon_type}"))
        return pygame.image.load(f"images/{pokemon_type}/{pokemon_image_path}")

    def generate_pokemones(self, general_pokemon_height: int = None, general_pokemon_width: int = None):
        pokemon_scale = 1
        for _ in range(self.n_poc):
            pokemon_type = random.choice(list(PokemonType)).name
            image = self.get_pokemon_image(pokemon_type)
            if general_pokemon_width and general_pokemon_height:
                image = pygame.transform.scale(image, (general_pokemon_width, general_pokemon_height))
            elif general_pokemon_height:
                image = pygame.transform.scale(image,
                                               (general_pokemon_height / image.get_height() * image.get_width(),
                                                general_pokemon_height))
            elif general_pokemon_width:
                image = pygame.transform.scale(image,
                                               (general_pokemon_width,
                                               general_pokemon_width / image.get_width() * image.get_height()))
            random_position: tuple[int] = (random.randint(int(self.rect.x + (image.get_width() * pokemon_scale) // 2),
                                                          int(self.rect.x + self.rect.width - (
                                                                      image.get_width() * pokemon_scale) // 2)),
                                           random.randint(int(self.rect.y + image.get_height() * pokemon_scale),
                                                          int(self.rect.y + self.rect.height - image.get_height() * pokemon_scale)))
            if pokemon_type == PokemonType.water.name:
                self.pokemons.add(WaterPokemon(name="wp",
                                               transform=Transform(position=Vector2(random_position[0],
                                                                                    random_position[1]),
                                                                   scale=Vector2(pokemon_scale, pokemon_scale)),
                                               image=image,
                                               atk=random.randint(1, World.MAX_POKEMON_ATK),
                                               df=random.randint(1, World.MAX_POKEMON_DF)))
            elif pokemon_type == PokemonType.fire.name:
                self.pokemons.add(FirePokemon(name="fp", transform=Transform(position=Vector2(random_position[0],
                                                                                              random_position[1]),
                                                                             scale=Vector2(pokemon_scale,
                                                                                           pokemon_scale)),
                                              image=image,
                                              atk=random.randint(1, World.MAX_POKEMON_ATK),
                                              df=random.randint(1, World.MAX_POKEMON_DF)))
            # elif t == 3:
            #     self.pokemons.add(GrassPokemon(name="gp", x=self.rect.center[0],
            #                                    y=self.rect.center[1], atk=random.randint(1, World.MAX_POKEMON_ATK),
            #                                    df=random.randint(1, World.MAX_POKEMON_DF)))
            # else:
            #     self.pokemons.add(ElectricPokemon(name="ep", x=self.rect.center[0],
            #                                       y=self.rect.center[1], atk=random.randint(1, World.MAX_POKEMON_ATK),
            #                                       df=random.randint(1, World.MAX_POKEMON_DF)))

    def draw(self, surface):
        self.horBorders.draw(surface)
        self.vertBorders.draw(surface)
        surface.set_clip(self.rect)
        self.pokemons.draw(surface)
        surface.set_clip(None)
        surface.blit(self.bg, self.bg_rect)

    def update(self):
        # hor_collision = pygame.sprite.groupcollide(self.pokemons, self.horBorders, False, False)
        # for p in hor_collision:
        #     p.vy = -p.vy
        #     pass
        # vert_collision = pygame.sprite.groupcollide(self.pokemons, self.vertBorders, False, False)
        # for p in vert_collision:
        #     p.vx = -p.vx
        #     pass
        self.pokemons.update()

    def catch_pokemon(self, pos):
        for pokemon in self.pokemons:
            if pokemon.rect.collidepoint(pos[0], pos[1]):
                self.pokemons.remove(pokemon)
                return pokemon
        # if len(self.pokemons.sprites()) > 0:
        #    pokemon = self.pokemons.sprites()[0]
        #    self.pokemons.remove(pokemon)
        #    return pokemon
        return None
