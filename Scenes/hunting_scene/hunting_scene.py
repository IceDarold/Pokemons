import os
import random
from enum import Enum

import pygame
from pygame import Vector2, Rect
from pygame.event import Event

import Pokemons.main_files.pokemons
from Pokemons.Base_classes import config
from Pokemons.Scenes.hunting_scene.Maze import Maze
from Pokemons.UI.base_ui.text import Text
from Pokemons.main_files import colors
from Pokemons.Base_classes.Player import Player
from Pokemons.Base_classes.Scene import Scene
from Pokemons.Base_classes.base_functions import check_collision_in_group
from Pokemons.Base_classes.game_data import GameData
from Pokemons.Base_classes.game_object import GameObject
from Pokemons.Base_classes.scene_manager import SceneManager
from Pokemons.Base_classes.transform import Transform
from Pokemons.main_files.pokemons import WaterPokemon, FirePokemon, GrassPokemon, ElectricPokemon
from Pokemons.main_files.trainer import Trainer
from Pokemons.UI.base_ui.button import Button

numbers_spr = {
    "ов": [0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 26, 27, 28, 29, 30],
    "": [1, 21, 31, 41, 51],
    "a": [2, 3, 4, 22, 23, 24, 32, 33, 34],
}


# noinspection PyTypeChecker
class HuntingScene(Scene):
    class PokemonType(Enum):
        fire = 0
        water = 1
        grass = 2
        electric = 3

    def __init__(self, name: str, game_data: GameData, player: Player, ring_boarders: Rect = None):
        super().__init__(name, game_data, fill_screen_color=colors.WHEAT)
        self.start_fight_button: Button = None
        self.number_of_bombs_text = None
        self.total_boms = 10
        self.number_of_pokemons_text: Text = None
        self.maze = None
        self.player: Player = player
        self.number_of_pokemons = 24
        self.pokemons = []
        self.trainers_list: list[Trainer] = []
        self.ring_boarders = ring_boarders
        # Чья сейчас очередь выбирать? 0 - игрок, 1 - бот
        self.choice_turn = 0
        self.create_trainers()
        self.player.collider_enter_actions.append(self.catch_pokemon)

    @Scene.event_decorator
    def events(self, e):
        self.player.actions(e)

    def create_trainers(self):
        trainer_1_choice = pygame.image.load(f'../images/trainers/{random.choice(os.listdir("../images/trainers"))}')
        trainer_2_choice = pygame.image.load(f'../images/trainers/{random.choice(os.listdir("../images/trainers"))}')

        trainers_scale = 0.5
        first_trainer_position = Vector2(trainer_1_choice.get_width() / 2 * trainers_scale,
                                         self.game_data.resolution[1] - trainer_1_choice.get_height() / 2
                                         * trainers_scale)
        second_trainer_position = Vector2(
            self.game_data.resolution[0] - trainer_2_choice.get_width() / 2 * trainers_scale,
            self.game_data.resolution[1] - trainer_2_choice.get_height() / 2 * trainers_scale)
        self.ring_boarders = Rect(0, 0, self.game_data.resolution[0], self.game_data.resolution[1])

    def mouse_button_down(self, e: Event):
        if self.choice_turn == self.player.hunting_turn_number:
            pokemon = check_collision_in_group(e.pos, self.pokemons)
            if pokemon:
                print("mouse")
                self.pokemons.remove(pokemon)
                self.player.add(pokemon)

    def catch_pokemon(self, game_object: GameObject):
        if isinstance(game_object, Pokemons.main_files.pokemons.Pokemon):
            print("YES", game_object in self.pokemons)
            self.pokemons.remove(game_object)
        else:
            print("NO")

    def bombs(self, game_object):
        if self.total_boms > 0 and pygame.key.get_pressed()[pygame.K_SPACE] and not isinstance(game_object,
                                                                                               Pokemons.main_files.pokemons.Pokemon):
            GameObject.all_objects.remove(game_object)
            self.total_boms -= 1

    @Scene.start_decorator
    def start(self):
        print("START_HUNTING")
        self.maze = Maze(config.cell_size, config.maze_size, config.maze_position, config.wall_width)
        self.generate_pokemones(60, 60, maze=self.maze)
        GameObject.all_objects.clear()
        self.number_of_pokemons_text = Text("Поймано 0 покемонов", colors.WHITE,
                                            Transform(position=(self.game_data.resolution[0] - 210, 50, 0)),
                                            300, 40)
        self.start_fight_button: Button = Button(colors.DARK_ORCHID,
                                                 Transform(position=(160, self.game_data.resolution[1] - 35, 0)),
                                                 300, 100, 50,
                                                 Text("Начать бой!", colors.RED, Transform(), 0, 0), self.start_fight)
        self.number_of_bombs_text: Text = Text("", colors.WHITE,
                                               Transform(position=(110, 50, 0)),
                                               300, 40)
        min_pokemons_text = Text(f"Соберите минимум {config.battle_team_size} покемонов", colors.WHITE,
                                 Transform(position=(160, self.game_data.resolution[1] - 100, 0)),
                                 300, 20)
        self.ui.add_new_UI_element(
            [self.number_of_pokemons_text, self.start_fight_button, self.number_of_bombs_text, min_pokemons_text])
        self.add_game_object(self.pokemons)
        self.add_game_object(self.trainers_list)
        self.add_game_object(self.player)
        self.add_game_object(self.maze.get_objects())
        # self.add_game_object(GameObject(Transform(position=(0, 0, 0)), rect=Rect(0, 0, 500, 300),
        #                                 render_type=GameObject.RenderType.image,
        #                                 image=pygame.image.load("images/br.jpg")))
        self.player.collider_enter_actions.append(self.bombs)

    def start_fight(self):
        if len(self.player.box) >= config.battle_team_size:
            SceneManager.load_new_scene("battle_scene")

    def generate_pokemones(self, general_pokemon_height: int = None, general_pokemon_width: int = None,
                           maze: Maze = None):
        max_pokemon_atk = 10
        max_pokemon_df = 10
        positions_in_maze_list = []
        non_generate_strings = (0, 0)
        for _ in range(self.number_of_pokemons):
            pokemon_type = random.choice(list(self.PokemonType)).name
            pokemon_image_path = random.choice(os.listdir(f"../images/{pokemon_type}"))
            image = pygame.image.load(f"../images/{pokemon_type}/{pokemon_image_path}")

            if general_pokemon_width and general_pokemon_height:
                image = pygame.transform.scale(image, (general_pokemon_width, general_pokemon_height))
            elif general_pokemon_height:
                image = pygame.transform.scale(image,
                                               (general_pokemon_height / image.get_height() * image.get_width(),
                                                general_pokemon_height))
            elif general_pokemon_width:
                image = pygame.transform.scale(image,
                                               (general_pokemon_width,
                                                general_pokemon_width / image.get_width() * image.get_height()))

            if maze:
                pos_in_maze = Vector2(random.randint(5, maze.maze_size.x - 5),
                                      maze.maze_size.y - random.randint(5, maze.maze_size.y - 5))
                if (maze.maze_size.x - non_generate_strings[0]) * (
                        maze.maze_size.y - non_generate_strings[1]) > self.number_of_pokemons:
                    print("Лабиринт слишком маленький!")
                else:
                    while pos_in_maze in positions_in_maze_list:
                        pos_in_maze = Vector2(random.randint(0, maze.maze_size.x - non_generate_strings[0]),
                                              random.randint(0, maze.maze_size.y - non_generate_strings[1]))
                positions_in_maze_list.append(pos_in_maze)
                random_position: tuple[int, int] = (pos_in_maze.x * maze.cell_size.x + maze.position.x,
                                                    pos_in_maze.y * maze.cell_size.y + maze.position.y)
            else:
                random_position: tuple[int, int] = (random.randint(int(self.ring_boarders.x + (image.get_width()) // 2),
                                                                   int(self.ring_boarders.x + self.ring_boarders.width - (
                                                                       image.get_width()) // 2)),
                                                    random.randint(int(self.ring_boarders.y + image.get_height()),
                                                                   int(self.ring_boarders.y + self.ring_boarders.height -
                                                                       image.get_height() // 2)))
            if pokemon_type == self.PokemonType.water.name:
                self.pokemons.append(WaterPokemon(name="wp",
                                                  transform=Transform(position=Vector2(random_position[0],
                                                                                       random_position[1])),
                                                  image=image,
                                                  atk=random.randint(1, max_pokemon_atk),
                                                  df=random.randint(1, max_pokemon_df)))
            elif pokemon_type == self.PokemonType.fire.name:
                self.pokemons.append(FirePokemon(name="fp", transform=Transform(position=Vector2(random_position[0],
                                                                                                 random_position[1])),
                                                 image=image,
                                                 atk=random.randint(1, max_pokemon_atk),
                                                 df=random.randint(1, max_pokemon_df)))
            elif pokemon_type == self.PokemonType.grass.name:
                self.pokemons.append(GrassPokemon(name="gp", transform=Transform(position=Vector2(random_position[0],
                                                                                                  random_position[1])),
                                                  image=image,
                                                  atk=random.randint(1, max_pokemon_atk),
                                                  df=random.randint(1, max_pokemon_df)))
            else:
                self.pokemons.append(ElectricPokemon(name="ep", transform=Transform(position=Vector2(random_position[0],
                                                                                                     random_position[
                                                                                                         1])),
                                                     image=image,
                                                     atk=random.randint(1, max_pokemon_atk),
                                                     df=random.randint(1, max_pokemon_df)))

    @Scene.main_loop_decorator
    def main_loop(self):
        # self.player.trainer.add(self.pokemons[-1])
        # self.pokemons.remove(self.pokemons[-1])
        self.player.move()
        box_len = len(self.player.box)
        right_fin = ""
        for key, value in numbers_spr.items():
            if box_len in value:
                right_fin = key
        if box_len >= config.battle_team_size:
            self.start_fight_button.color = colors.GREEN
        self.number_of_pokemons_text.text = f"Пойман{'' if box_len == 1 else 'o'} {box_len} покемон{right_fin}"
        self.number_of_bombs_text.text = f"Бомбы: {self.total_boms}"
