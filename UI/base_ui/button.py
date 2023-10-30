import pygame
from magic_filter.operations import function
from pygame import Surface

from Pokemons.Base_classes.transform import Transform
from Pokemons.UI.base_ui.UI import UIElement
from Pokemons.UI.base_ui.text import Text


class Button(UIElement):
    def __init__(self, color: tuple[int, int, int], transform: Transform, length: float, width: float,
                 height: float, text: Text, button_event: function,
                 fit_text_to_button: bool = True, name="Button", button_params: list = [], interactive: bool = True):
        self.rect = None
        self.color = color
        self.width = width
        self.length = length
        self.height = height
        self.text = text
        self.button_params = button_params
        self.pressed_event = button_event
        self.interactive = interactive
        self.fit_text_to_button = fit_text_to_button
        if fit_text_to_button:
            self.text.transform = transform
            self.text.width = self.length
            self.text.height = self.height
        super().__init__(transform=transform, name=name)
        self.rect = pygame.Rect(self.get_transform().position.x - length // 2,
                                self.get_transform().position.y - height // 2, self.length, self.height)

    def draw(self, surface: Surface):
        self.draw_button(surface)
        self.text.draw(surface)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.pressed(event.pos):
            self.pressed_event(*self.button_params)

    def draw_button(self, surface: Surface):
        my_s = pygame.Surface((self.length, self.height))
        my_s.fill(self.color)
        surface.blit(my_s, self.rect)
        return
        # for i in range(1, 10):
        #     s = pygame.Surface((self.length + (i * 2), self.height + (i * 2)))
        #     s.fill(self.color)
        #     alpha = (255 / (i + 2))
        #     if alpha <= 0:
        #         alpha = 1
        #     s.set_alpha(alpha)
        #     pygame.draw.rect(s, self.color, (self.get_transform().position.x - i, self.get_transform().position.y - i,
        #                                      self.length + i, self.height + i), int(self.width))
        #     surface.blit(s, (self.get_transform().position.x - i, self.get_transform().position.y - i))
        # pygame.draw.rect(surface, self.color, (self.get_transform().position.x, self.get_transform().position.y,
        #                                             self.length, self.height), 0)
        # pygame.draw.rect(surface, (190, 190, 190), (self.get_transform().position.x, self.get_transform().position.y,
        #                                                  self.length, self.height), 1)

    def pressed(self, mouse):
        if not self.interactive:
            return
        if mouse[0] > self.rect.topleft[0]:
            # print("topleftx")
            if mouse[1] > self.rect.topleft[1]:
                # print("toplefty")
                if mouse[0] < self.rect.bottomright[0]:
                    # print("bottomx")
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
        return False
