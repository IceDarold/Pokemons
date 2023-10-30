import pygame
from pygame import Surface

from Pokemons.Base_classes.transform import Transform
from Pokemons.UI.base_ui.UI import UIElement


class Text(UIElement):
    def __init__(self, text: str, text_color: tuple[int, int, int],
                 transform: Transform = Transform(), width: float = 0, height: float = 0, font: str = "../../fonts/JosefinSans-VariableFont_wght.ttf", name="text"):
        self.text: str = text
        self.text_color = text_color
        self.transform = transform
        self.width = width
        self.height = height
        self.font = font
        super().__init__(transform=transform, name=name)

    def draw(self, surface: Surface):
        font_size = int(self.height * self.transform.scale.x)
        try:
            my_font = pygame.font.Font(self.font, font_size)
        except FileNotFoundError:
            my_font = pygame.font.SysFont(self.font, font_size)
        my_text = my_font.render(self.text, 1, self.text_color)
        rect = my_text.get_rect(center=self.transform.position.xy)
        surface.blit(my_text, rect)
