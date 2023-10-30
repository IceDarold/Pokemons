from pygame import Vector2
from pygame.sprite import Sprite, Group


def check_collision_in_group(position: Vector2 | tuple[int, int], object_list: list | Group):
    if isinstance(object_list, Group):
        object_list = object_list.sprites()
    if isinstance(position, Vector2):
        position = position.xy
    for col_object in object_list:
        print(position, col_object.rect)
        if col_object.rect.collidepoint(position[0], position[1]):
            return col_object
    return None
