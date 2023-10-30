from pygame import Surface

from Pokemons.Base_classes.game_object import GameObject
from Pokemons.Base_classes.movable_object import MovableObject
from Pokemons.Base_classes.transform import Transform
from Pokemon import Pokemon
from Pokemons.UI.base_ui.image import Image
from Pokemons.UI.base_ui.text import Text


class Trainer(MovableObject):
    def __init__(self, transform: Transform, image: Surface, speed: int, move_through_ring=False,
                 resolution: tuple[int, int] = None):
        self.box: list[Pokemon] = []
        self.dict_box: dict[Image, Pokemon] = {}
        """
        Словарь с Pokemons и Image, которые соответствуют покемонам
        """
        self.wins: int = 0
        common_choice = MovableObject.MoveThroughType.change_side
        super().__init__(transform=transform, image=image, speed=speed, move_through_ring=move_through_ring,
                         resolution=resolution, move_through_keys=(common_choice, common_choice, common_choice,
                                                                   common_choice))

    def add(self, pokemon: Pokemon, is_dict: bool = False):
        """
        Добавляет покемена в box
        :param pokemon: покемон, которого нужно добавить
        :return:
        """
        if is_dict:
            self.dict_box[Image(pokemon.transform, pokemon.get_img(), rect=pokemon.rect)] = pokemon
        else:
            self.box.append(pokemon)

    def best_team(self, n):
        return self.box[:n]
