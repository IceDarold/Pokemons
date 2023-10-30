import pygame.image
from pygame import Surface, Vector2, SurfaceType, Rect

from Pokemons.Base_classes.transform import Transform
from Pokemons.UI.base_ui.UI import UIElement


class Image(UIElement):
    def __init__(self, transform: Transform, image: Surface | SurfaceType,
                 pixel_size: Vector2 | tuple[int, int] = None, layer: int = 0, rect: Rect = None,
                 name: str = "new Image"):
        super().__init__(transform=transform, name=name, layer=layer)
        self.image = image
        self._pixel_size = Vector2(image.get_width(), image.get_height())
        if pixel_size:
            self.change_pixel_size(pixel_size)
        self.change_size(transform.scale)
        if rect:
            self.rect = rect
        else:
            self.rect = self.image.get_rect(center=transform.position.xy)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def change_size(self, new_size: Vector2):
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * new_size.x,
                                                         self.image.get_height() * new_size.y))

    def change_pixel_size(self, new_pixel_size: Vector2):
        self.image = pygame.transform.scale(self.image, new_pixel_size)
        print("PS", self.image.get_rect())
        self.rect = self.image.get_rect(center=self.get_transform().position.xy)
        print("PS", self.rect)
        self._pixel_size = new_pixel_size

    def change_position(self, new_position: Vector2):
        self._transform.position = new_position
        self.rect = self.image.get_rect(center=self.get_transform().position.xy)

    def get_pixel_size(self):
        return self._pixel_size.copy()
