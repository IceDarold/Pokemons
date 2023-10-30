import pygame
from pygame import Vector2
from pygame.sprite import Group, Sprite

from Lessons.Pokemons import Pokemon
from Lessons.Pokemons.Base_classes.base_functions import check_collision_in_group
from Lessons.Pokemons.Base_classes.transform import Transform
from Lessons.Pokemons.UI import UI
from Lessons.Pokemons.UI.image import Image


def choice_team(player_team: list[Pokemon], first_pokemon_position: Vector2, pokemons_in_row: int) -> (Group, Vector2):
    """
     Настраивает размещение покемонов в окошке выбора покемонов для боя
    :param player_team: список покемонов, среди которых нужно выбирать команду для боя
    :param first_pokemon_position: позиция покемона в левом верхнем углу меню для выбора
    :param pokemons_in_row: количество покемонов в строчке
    :return: Group, состоящую из покемонов с настроенной позицией и размер всего размещения
    """
    box_group = Group()
    index = 0
    last_position: Vector2 = first_pokemon_position.copy()
    for pokemon in player_team:
        if index % pokemons_in_row == 0 and index != 0:
            height_list = []
            for pokemon_height in player_team:
                height_list.append(pokemon_height.image.get_height())
            last_position.x = first_pokemon_position.x
            last_position.y += max(height_list)
        last_position += Vector2(box_group.sprites()[-1].rect.width // 2 if index % pokemons_in_row != 0 else 0,
                                 0)
        last_position += Vector2(pokemon.rect.width // 2, 0)
        pokemon.rect.center = last_position
        #        pokemon.vx = pokemon.vy = 0
        box_group.add(pokemon)
        index += 1
    last_right_sprite = player_team[-1] if len(player_team) <= pokemons_in_row else player_team[pokemons_in_row - 1]
    # Берем края всей композиции спрайтов и вычитаем их, получая общий размер композиции
    size = Vector2((last_right_sprite.rect.x + last_right_sprite.rect.width / 2) -
                   (first_pokemon_position.x - player_team[0].rect.width / 2),
                   (player_team[-1].rect.y + player_team[-1].rect.height / 2) -
                   (player_team[0].rect.y - player_team[0].rect.width / 2))
    center = size / 2 + player_team[0].rect.center - Vector2(player_team[0].rect.width / 2,
                                                             player_team[0].rect.height / 2)

    return box_group, size, center
