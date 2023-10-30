import pygame
from pygame import Vector2, Surface

from Pokemons.Base_classes.transform import Transform
from Pokemons.UI.base_ui import UI
from Pokemons.UI.base_ui.UI import UIElement


class Rect(UIElement):
    def __init__(self, transform: Transform, width: int, height: int, color: tuple[int, int, int],
                 left_top: Vector2 | Transform = None, name: str = "new Rect"):
        self.transform = transform
        self.width = width
        self.height = height
        self.color = color
        if left_top:
            self.transform.position = left_top + Vector2(width // 2, height // 2)
        super().__init__(transform=transform, name=name)

    def draw(self, surface: Surface):
        pygame.draw.rect(surface=surface, width=self.width, color=self.color,
                         rect=(self.transform.position.x - self.width / 2,
                               self.transform.position.y - self.height / 2,
                               self.width, self.height))
