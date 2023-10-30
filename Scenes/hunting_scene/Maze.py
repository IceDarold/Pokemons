import random
import sys

import pygame.image
from pygame import Rect, Vector2

from Pokemons.Base_classes.game_object import GameObject
from Pokemons.Scenes.hunting_scene.maze_cell import MazeCell


class Maze:
    def __init__(self, cell_size: tuple[int, int] | Vector2, maze_size: tuple[int, int],
                 position: Vector2 | tuple[int, int], wall_width: int,
                 is_braid: bool = False):
        """
        :param cell_size: размер одной клетки лабиринта
        :param maze_size: размер лабиринта. первая компонента - количество строк. вторая - количество стобцов
        :param position: глобальная позиция лабиринта
        :param is_braid: является ли лабиринт плетеным?
        """""
        self.cell_size: Vector2 = Vector2(cell_size)
        self.maze_size = Vector2(maze_size)
        self.wall_width = wall_width
       # print(self.maze_size, self.cell_size, position)
        self.maze: list[[MazeCell]] = [[]]
        self.maze_objects: list[GameObject] = []
        self.position = position if isinstance(position, Vector2) else Vector2(position[0], position[1])
        print(self.position)
        self.is_braid = is_braid
        self.generate()
        self.make_format(bottom_string=False)
        self.max_braid_walls: int = 2

    def get_objects(self) -> list[GameObject]:
        return_list = []
        for row in range(int(self.maze_size.x)):
            for col in range(int(self.maze_size.y)):
                for wall in self.maze[row][col].get_object():
                    return_list.append(wall)
        return return_list

    def generate(self):
        """
        Генерирует лабиринт при помощи алгоритма Эллера. https://habr.com/ru/articles/176671/
        :return:
        """
        self.maze: list[[MazeCell]] = [[MazeCell(Vector2(col, self.maze_size.y - row),
                                                self.position, self.cell_size, self.wall_width)
                                        for col in range(int(self.maze_size.y))] for row in
                                       range(int(self.maze_size.x))]
        for row in range(int(self.maze_size.x)):
            #Список множеств строки
            row_list: list[list[MazeCell]] = [[]]
            for col in range(int(self.maze_size.y)):
                if col == 0:
                    row_list[-1].append(self.maze[row][col])
                    continue
                #0 - сносим стенку, 1 - нет
                if random.randint(0, 1) == 0:
                    self.maze[row][col].left_wall = False
                    row_list[-1].append(self.maze[row][col])
                else:
                    row_list.append([self.maze[row][col]])
            for row_set in row_list:
                if self.is_braid:
                    for i in range(random.randint(1, self.max_braid_walls)):
                        random.choice(row_set).top_wall = False
                else:
                    random.choice(row_set).top_wall = False

    def make_format(self, bottom_string: bool = True, top_sting: bool = True, left_string: bool = True,
                    right_string: bool = True, garbage_bottom_string = True):
        """
        Дополняем боковые стены
        :param bottom_string: Нужно ли дополнять нижнюю стену?
        :param top_sting: Нужно ли дополнять верхнюю стену?
        :param left_string: Нужно ли дополнять левую стену?
        :param right_string: Нужно ли дополнять правую стену?
        :return:
        """
        if bottom_string or garbage_bottom_string:
            for i in self.maze[0]:
                if garbage_bottom_string:
                    i.left_wall = False
                if bottom_string:
                    i.top_wall = True

        if top_sting:
            for i in self.maze[-1]:
                i.top_wall = True

        if left_string or right_string:
            for i in range(int(self.maze_size.y)):
                if left_string:
                    if i != 0:
                        self.maze[i][0].left_wall = True
                if right_string:
                    if i != 0:
                        self.maze[i][-1].left_wall = True
                    self.maze[i][-1].top_wall = False

    def create_entrances(self, bottom_string: tuple[bool, int] = (False, 0), top_sting: tuple[bool, int] = (False, 0),
                         left_string: tuple[bool, int] = (True, 1), right_string: tuple[bool, int] = (True, 1)):
        if top_sting[0]:
            pass

