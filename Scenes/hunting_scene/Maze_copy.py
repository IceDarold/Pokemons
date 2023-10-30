import random

import pygame.image
from pygame import Rect, Vector2

from Pokemons.Base_classes.game_object import GameObject


class Maze:
    def __init__(self, cell_size, rows_and_cols: tuple[int, int], position: Vector2 | tuple[int, int]):
        self.cell_size = cell_size
        self.rows_and_cols = rows_and_cols
        self.maze = [[0 for _ in range(self.rows_and_cols[1])] for _ in range(self.rows_and_cols[0])]
        self.maze_objects: list[GameObject] = []
        self.position = position if isinstance(position, Vector2) else Vector2(position[0], position[1])
        self.position -= Vector2(cell_size * rows_and_cols[1] // 2, cell_size * rows_and_cols[0] // 2)
        print(self.position)
        self.generate_maze()

    def generate_maze(self):
        def generate_maze_func(row, col):
            self.maze[row][col] = 1
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(directions)
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < self.rows_and_cols[0] and 0 <= new_col < self.rows_and_cols[1] and self.maze[new_row][
                    new_col] == 0:
                    self.maze[row + dr // 2][col + dc // 2] = 1
                    generate_maze_func(new_row, new_col)

        generate_maze_func(0, 0)
        for row_i in range(self.rows_and_cols[0]):
            for col_i in range(self.rows_and_cols[1]):
                if self.maze[row_i][col_i] == 1:
                    self.maze_objects.append(GameObject(render_type=GameObject.RenderType.rect,
                                                        rect=Rect(self.position.x + col_i * self.cell_size,
                                                                  self.position.y + row_i * self.cell_size,
                                                                  self.cell_size, self.cell_size)))

