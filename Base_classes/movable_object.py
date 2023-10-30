from enum import Enum

from pygame import Vector3, Surface, Vector2

from Pokemons.Base_classes.Camera import Camera
from Pokemons.Base_classes.game_object import GameObject
from Pokemons.Base_classes.transform import Transform


class MovableObject(GameObject):
    """
    Базовый класс для двигающихся объектов. Предоставляет необходимый функционал
    """

    class MoveThroughType(Enum):
        nothing = 0
        block = 1
        change_side = 2

    def __init__(self, transform: Transform, speed: float, sprint: bool = False, image: Surface = None,
                 move_through_ring: bool = False, resolution: tuple[int, int] = None,
                 move_through_keys: tuple[MoveThroughType, MoveThroughType, MoveThroughType, MoveThroughType] =
                 (MoveThroughType.block, MoveThroughType.block, MoveThroughType.block, MoveThroughType.block)):
        """

        :param transform:
        :param speed: скорость обЪекта
        :param sprint:
        :param image:
        :param move_through_ring: если объект достиг границы экрана, переместится ли он на другую сторону экрана
        :param resolution: разрешение экрана
        :param move_through_keys: параметр перемещения на другюю сторону экрана для каждой из стороны.
        0 - левая стороны
        1 - правая
        2 - верхняя
        3 - нижняя
        """
        self.move_through_ring = move_through_ring
        self.move_through_keys = move_through_keys
        assert not self.move_through_ring or self.move_through_ring and resolution, (
            "Если Movable object может перемещаться через "
            "границы игрового поля, нужно передать resolution!")
        self._speed = speed
        self.resolution = resolution
        self._move_direction = Vector2(0, 0)
        self.sprint: bool = sprint
        self.sprint_coefficient = 2
        super().__init__(transform, image=image)

    def move(self, move_direction=None):
        if not move_direction:
            move_direction = self._move_direction
        direction = move_direction * self._speed * (self.sprint_coefficient if self.sprint else 1)
        if GameObject.check_colider(self, self.rect.move(direction)):
            return
        Camera.move_camera(-direction, [self])
        return
        move_rect = self.rect.move(direction.x, direction.y)
        if self.move_through_ring:
            if move_rect.x < 0:
                if self.move_through_keys[0] == MovableObject.MoveThroughType.block:
                    return
                elif self.move_through_keys[0] == MovableObject.MoveThroughType.change_side:
                    if move_rect.x + move_rect.width < 0:
                        move_rect.x = self.resolution[0] + move_rect.width
                        self.transform.position.x = self.resolution[0] + move_rect.width
            if move_rect.x + move_rect.width > self.resolution[0]:
                if self.move_through_keys[1] == MovableObject.MoveThroughType.block:
                    return
                elif self.move_through_keys[1] == MovableObject.MoveThroughType.change_side:
                    if move_rect.x - move_rect.width > self.resolution[0]:
                        move_rect.x = -move_rect.width
                        self.transform.position.x = -move_rect.width
            if move_rect.y < 0:
                if self.move_through_keys[2] == MovableObject.MoveThroughType.block:
                    return
                elif self.move_through_keys[2] == MovableObject.MoveThroughType.change_side:
                    if move_rect.y + move_rect.height < 0:
                        move_rect.y = self.resolution[1] + move_rect.height
                        self.transform.position.y = self.resolution[1] + move_rect.height
            if move_rect.y + move_rect.height > self.resolution[1]:
                if self.move_through_keys[3] == MovableObject.MoveThroughType.block:
                    return
                elif self.move_through_keys[3] == MovableObject.MoveThroughType.change_side:
                    if move_rect.y - move_rect.height > self.resolution[1]:
                        move_rect.y = -move_rect.height
                        self.transform.position.y = -move_rect.height
        self.rect = move_rect
        self.transform.position += Vector3(direction.x, direction.y, 0)
