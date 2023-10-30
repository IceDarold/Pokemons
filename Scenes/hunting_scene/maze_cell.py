from pygame import Vector2, Rect

from Pokemons.Base_classes.game_object import GameObject
from Pokemons.Base_classes.transform import Transform


class MazeCell:
    def __init__(self, position_in_maze: Vector2, maze_position: Vector2 | tuple, cell_size: Vector2,
                 wall_width: int,
                 left_wall: bool = True, top_wall: bool = True):
        self.left_wall = left_wall
        self.top_wall = top_wall
        self.maze_position = Vector2(maze_position)
        self.position_in_maze = Vector2(position_in_maze)
        self.cell_size = Vector2(cell_size)
        # Размер стен. x - ширина, y - длина
        self.wall_width: int = wall_width

    def get_object(self) -> (GameObject, GameObject):
        cell_global_pos = self.get_global_position()
        left_wall_obj = GameObject()
        if self.left_wall:
            left_wall_center = Vector2(cell_global_pos.x - self.cell_size.x // 2 + self.wall_width // 2,
                                       cell_global_pos.y - self.wall_width)
            left_wall_obj = GameObject(transform=Transform(
                position=left_wall_center),
                render_type=GameObject.RenderType.rect,
                rect=Rect(left_wall_center.x - self.wall_width // 2, left_wall_center.y - self.cell_size.y // 2,
                          self.wall_width, self.cell_size.y + self.wall_width))
        else:
            left_wall_obj.active = False

        top_wall_obj = GameObject()
        if self.top_wall:
            top_wall_center = Vector2(cell_global_pos.x,
                                      cell_global_pos.y - self.cell_size.y // 2 - self.wall_width // 2)
            top_wall_obj = GameObject(transform=Transform(
                position=top_wall_center),
                render_type=GameObject.RenderType.rect,
                rect=Rect(top_wall_center.x - self.cell_size.x // 2, top_wall_center.y - self.wall_width // 2,
                          self.cell_size.x, self.wall_width))
        else:
            top_wall_obj.active = False
        return left_wall_obj, top_wall_obj

    def get_global_position(self) -> Vector2:
        return Vector2(self.position_in_maze.x * self.cell_size.x + self.maze_position.x - self.cell_size.x,
                       self.position_in_maze.y * self.cell_size.y + self.maze_position.y - self.cell_size.y)
