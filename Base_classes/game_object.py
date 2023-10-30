from enum import Enum

import pygame
from pygame import Surface, Rect
from pygame.sprite import Sprite

from Pokemons.main_files import colors
from Pokemons.Base_classes.transform import Transform


class GameObject(Sprite):
    all_objects: list = []

    class RenderType(Enum):
        image = 0
        rect = 1

    def __init__(self, transform: Transform = Transform(), rect: Rect = None, image: Surface = None, active=True,
                 render_type: RenderType = RenderType.image):
        """
        Базовый класс для всех игровых объектов
        :param transform: параметр типа Transform, отвечающий за все параметры размещения
        объекта в мировом пространстве
        :param image_path: изображение объекта
        """
        self.transform: Transform = transform
        self.render_type = render_type
        self._img: Surface = None
        if render_type == GameObject.RenderType.image and image:
            self._img: Surface = image.convert_alpha()
            print(self._img.get_size())
            self._img = pygame.transform.scale(self._img, (self._img.get_width() * transform.scale.x,
                                                           self._img.get_height() * transform.scale.y))
            self.rect = self._img.get_rect()
            self.rect.center = transform.position.xy
        if rect:
            self.rect = rect
            if not transform:
                self.transform.position = rect.center
            if self._img and self.render_type == GameObject.RenderType.image:
                self._img = pygame.transform.scale(self._img, self.rect.size)
        self.active = active
        self.drawed = False
        self.global_position = (0, 0)
        super().__init__()

    def collider_enter(self, game_object):
        pass

    def draw(self, surface: Surface):
        if not self.active:
            return
        global_rect = self.get_global_rect()
        if self.render_type == GameObject.RenderType.image:
            try:
                surface.blit(self._img, global_rect)
            except AttributeError:
                print(f"У обЪекта {self} отсутствует image. Отображение невозможно!")
                return
        elif self.render_type == GameObject.RenderType.rect:
            if not self.drawed:
                print("Wall", self.rect)
            self.drawed = True
            pygame.draw.rect(surface, colors.PALE_TURQUOISE, global_rect)

    def get_img(self):
        return self._img

    def get_global_rect(self, rect=None) -> Rect:
        if rect:
            return rect.move(self.global_position[0], self.global_position[1])
        else:
            return self.rect.move(self.global_position[0], self.global_position[1])

    def get_rect(self) -> Rect:
        return self.rect

    @staticmethod
    def check_colider(gameobject, rect: Rect = None):
        """
        Проверяет задевает ли gameobject какие-то другие объекты
        :param gameobject: объект, которые мы проверяем
        :param rect: если нужно проверить не текущий rect объекта, а какой-то другой,
        то можно передать этот rect необязательным параметром
        :return: возвращает gameobject, который задевает переданный в функцию объект или None
        """
        global_rect = gameobject.get_global_rect(rect)
        for game_object in GameObject.all_objects:
            if game_object == gameobject or not game_object.active:
                continue
            global_rect_object = game_object.get_global_rect()
            if global_rect.colliderect(global_rect_object):
                print(f"Задел! {game_object} {gameobject}, Rect {rect}, game_object.rect {game_object.rect})")
                game_object.collider_enter(gameobject)
                gameobject.collider_enter(game_object)
                return game_object
        return None
