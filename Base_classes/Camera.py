from pygame import Vector2

from Pokemons.Base_classes.game_object import GameObject


class Camera:
    _position = (0, 0)

    @staticmethod
    def move_camera(distance: tuple[int, int] | Vector2, except_objects: list[GameObject] = None):
        Camera._position += (distance if isinstance(distance, Vector2) else Vector2(distance.x, distance.y))
        for game_object in GameObject.all_objects:
            if except_objects and game_object in except_objects:
                continue
            game_object.global_position += distance

    @staticmethod
    def get_position() -> Vector2:
        return Vector2(Camera._position)
