from pygame import Vector2, Vector3, Rect


class Transform:
    def __init__(self, position: Vector2 | Vector3 | tuple[float, float, float] | Rect = Vector3(0, 0, 0), rotation: Vector2 | Vector3 = Vector3(0, 0, 0),
                 scale: Vector2 | Vector3 | tuple[float, float, float] = Vector3(1, 1, 1)):
        if isinstance(position, Rect):
            self.position = position.center
        if isinstance(scale, tuple):
            self.scale = Vector3(scale)
        else:
            self.scale = scale if isinstance(scale, Vector3) else Vector3(scale.x, scale.y, 0)
        if isinstance(position, tuple):
            self.position = Vector3(position[0], position[1], position[2])
        else:
            self.position: Vector3 = position if isinstance(position, Vector3) else Vector3(position.x, position.y, 0)
        self.rotation = rotation if isinstance(rotation, Vector3) else Vector3(rotation.x, rotation.y, 0)

    def copy(self):
        return Transform(position=self.position, scale=self.scale, rotation=self.rotation)

    def __str__(self):
        return f"Position: {self.position}\nScale: {self.scale}\nRotation: {self.rotation}"