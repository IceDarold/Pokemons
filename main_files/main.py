import os.path
import sys

import pygame.display
from pygame import Vector3

from Pokemons.Base_classes import config
from Pokemons.Base_classes.Player import Player
from Pokemons.Base_classes.game_data import GameData
from Pokemons.Base_classes.maze_data import MazeData
from Pokemons.Base_classes.scene_manager import SceneManager
from Pokemons.Scenes.bad_scene.bag_scene import BagScene
from Pokemons.Scenes.battle_scene.battle_scene import BattleScene
from Pokemons.Scenes.hunting_scene.hunting_scene import HuntingScene
from Pokemons.Scenes.main_menu.main_menu import MainMenuScene
from Pokemons.Scenes.waiting_room.waiting_room import WaitingRoomScene
from Pokemons.online.client import Client
from Pokemons.online.server import Server
from world import *
from battle import *


class Game:
    class GameStatus(Enum):
        START = 0
        HUNT = 1
        CHOICE_TEAM = 2
        BATTLE = 3

    def __init__(self):
        self.game_data: GameData = None
        self._running = True
        self.game_status = self.GameStatus.START
        self.full_screen: bool = False

    def end_game(self):
        self._running = False

    def check_config(self):
        if config.battle_team_size <= 0:
            raise TypeError("Размер команды не может быть меньше или равен 0! Измените данные в config.py")
        if config.maze_size[0] < 3 or config.maze_size[1] < 3:
            raise TypeError("Размер лабиринта не может быть меньше (3, 3)! Измените данные в config.py")

    def main(self):
        self.check_config()
        pygame.init()
        pygame.mixer.init()
        resolution = (1000, 500)
        screen = pygame.display.set_mode((0, 0) if self.full_screen else resolution,
                                         pygame.FULLSCREEN if self.full_screen else 0)
        resolution = pygame.display.get_window_size()
        pygame.display.set_caption("Pokemons")
        clock = pygame.time.Clock()
        player_pos = Vector3(0, 1700, 0)
        player: Player = Player(transform=Transform(scale=(1, 1, 1), position=player_pos),
                                move_through_ring=True, resolution=resolution)
        maze_data = MazeData(random.randint(0, 100000))
        server = Server(maze_data)
        client = Client(maze_data)
        self.game_data = GameData(60, screen, clock, resolution, False, server, client)
        main_menu = MainMenuScene("main_menu", self.game_data)
        bag_scene = BagScene("bag_scene", self.game_data)
        hunting_scene = HuntingScene("hunting_scene", self.game_data, player)
        battle_scene = BattleScene("battle_scene", self.game_data, player)
        waiting_room_scene = WaitingRoomScene("waiting_room", self.game_data)
        SceneManager.add_scenes([main_menu, hunting_scene, battle_scene, waiting_room_scene, bag_scene])
        SceneManager.load_new_scene(main_menu)
        self.game_status = self.GameStatus.START


if __name__ == "__main__":
    game = Game()
    try:
        game.main()
        5 % 0
    except OverflowError as ex:
        print("Error:", ex)
        SceneManager.load_new_scene("bag_scene")
