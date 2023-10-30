import os
from enum import Enum
import random

import pygame
from pygame import Vector2, Surface
from pygame.event import Event

from Pokemons.Base_classes import config
from Pokemons.Base_classes.base_functions import check_collision_in_group
from Pokemons.main_files import colors
from Pokemons.Base_classes.Player import Player
from Pokemons.Base_classes.Scene import Scene
from Pokemons.Base_classes.game_data import GameData
from Pokemons.Base_classes.transform import Transform
from Pokemons.Scenes.battle_scene.UI.battle_scene_ui import draw_check_frame, choice_team
from Pokemons.UI.base_ui.button import Button
from Pokemons.UI.base_ui.image import Image
from Pokemons.UI.base_ui.text import Text
from Pokemons.main_files.Pokemon import Pokemon
from Pokemons.main_files.pokemons import WaterPokemon, GrassPokemon, ElectricPokemon, FirePokemon
from Pokemons.main_files.trainer import Trainer


class BattleScene(Scene):
    class BattleState(Enum):
        PREPARATION = 0
        FIGHT = 1
        CHOICE = 2
        ATTACK = 3

    def __init__(self, name: str, game_data: GameData, player: Player, battle_team_size: int = 5):
        super().__init__(name, game_data, fill_screen_color=colors.WHEAT)
        self.attack_text = None
        self.second_trainer: Trainer = None
        self.image_list: dict[Image, Pokemon] = {}
        self.player: Player = player
        self.battle_status = self.BattleState.PREPARATION
        self.chosen_pokemons: list[Image] = []
        """
         Список покемонов, которых выбрал игрок
        """
        self.stable_frames_dict = {}
        self.attack_pokemon: Pokemon = None
        """
        Покемон, который будет атаковать
        """
        self.defensive_pokemon: Pokemon = None
        """
        Покемон, который будет защищаться
        """
        self.attack_button: Button = None

    def mouse_motion(self, e: Event):
        if self.battle_status == self.BattleState.PREPARATION:
            draw_check_frame(e.pos, list(self.image_list.values()),
                             ui=self.ui, frame_image=Image(image=pygame.image.load(
                    "../images/UI/free-icon-selection-symbol-for-interface-of-a-square-of"
                    "-broken-line-32454.png"),
                    transform=Transform(scale=Vector2(1, 1)), layer=1,
                    name="frame_image"))
        elif self.battle_status == self.BattleState.FIGHT:
            draw_check_frame(e.pos, list(self.second_trainer.dict_box.values()),
                             ui=self.ui, frame_image=Image(image=pygame.image.load(
                    "../images/UI/free-icon-selection-symbol-for-interface-of-a-square-of"
                    "-broken-line-32454.png"),
                    transform=Transform(scale=Vector2(1, 1)), layer=1,
                    name="frame_image"))
            draw_check_frame(e.pos, list(self.convert_image_to_pokemon(self.chosen_pokemons, self.image_list)),
                             ui=self.ui, frame_image=Image(image=pygame.image.load(
                    "../images/UI/free-icon-selection-symbol-for-interface-of-a-square-of"
                    "-broken-line-32454.png"),
                    transform=Transform(scale=Vector2(1, 1)), layer=1,
                    name="frame_image"))

    def any_key_pressed(self, e: Event):
        if self.attack_button.interactive and e.key == pygame.K_RETURN:
            self.attack()

    def attack(self):
        self.attack_pokemon.attack(self.defensive_pokemon)
        print("Battle result:", self.attack_pokemon, self.defensive_pokemon)
        print("ATTACK!")
        self.check_alive(True)
        self.check_alive(False)

    def mouse_button_down(self, e: Event):
        if self.battle_status == self.BattleState.PREPARATION:
            collider_image: Image = None
            for image, pokemon in self.image_list.items():
                if image.rect.collidepoint(e.pos[0], e.pos[1]):
                    collider_image = image
            if collider_image:
                if collider_image not in self.chosen_pokemons:
                    if len(self.chosen_pokemons) < config.battle_team_size:
                        print("YEAH")
                        self.chosen_pokemons.append(collider_image)
                        print("BOB", self.chosen_pokemons[-1] in self.image_list.keys())
                        image = Image(image=pygame.image.load(
                            "../images/UI/free-icon-selection-symbol-for-interface-of-a-square-of-broken-line-32454.png"),
                            transform=Transform(scale=Vector2(1, 1)),
                            layer=1,
                            name="frame image stable")
                        self.stable_frames_dict[collider_image] = image
                        draw_check_frame(position=collider_image.rect.center, ui=self.ui,
                                         pokemons=list(self.image_list.keys()),
                                         frame_image=image)
                        if len(self.chosen_pokemons) == config.battle_team_size:
                            ready_button: Button = Button(color=(107, 142, 35), width=0,
                                                          text=Text("Start", (255, 255, 255)),
                                                          button_event=self.start_battle,
                                                          transform=Transform(position=Vector2(400,
                                                                                               400),
                                                                              scale=Vector2(1, 1)),
                                                          height=100,
                                                          length=200, name="start fight button")
                            self.ui.add_new_UI_element(ready_button)
                else:
                    self.chosen_pokemons.remove(collider_image)
                    self.ui.remove_UI_element(self.stable_frames_dict[collider_image])
                    self.ui.remove_UI_element("start fight button")
                for i in self.chosen_pokemons:
                    print("CHP0", i in self.image_list.keys())
        if self.battle_status == self.BattleState.CHOICE:
            collider_image_attack: Image = check_collision_in_group(e.pos, self.chosen_pokemons)
            for i in self.chosen_pokemons:
                for j in self.image_list.keys():
                    print("CHP", i in self.image_list.keys())
            print("CHECK", collider_image_attack in self.image_list.keys())
            # for image in self.chosen_pokemons:
            #     if image.rect.collidepoint(e.pos[0], e.pos[1]):
            #         collider_image_attack = image
            collider_image_defensive: Image = check_collision_in_group(e.pos, list(self.second_trainer.dict_box.keys()))
            if collider_image_attack:
                # Если при нажатии игрок нажал на какого-то покемона, то мы удаляем рамку на предыдущем выборе.
                # Даже если это был тот же покемон, мы тоже удаляем рамку, чтобы отменить выбор
                if self.attack_pokemon is None:
                    previous_attack = None
                else:
                    previous_attack = self.convert_image_to_pokemon([self.attack_pokemon], self.image_list, True)
                if self.attack_pokemon:
                    print("ДАААААААААААА")
                    self.ui.remove_UI_element("attack pokemon frame image stable")
                    self.attack_pokemon = None
                # Если игрок все-таки выбрал нового покемона
                if previous_attack != collider_image_attack:
                    print("Не равен")
                    self.attack_pokemon = self.image_list[collider_image_attack]
                    image = Image(image=pygame.image.load(
                        "../images/UI/free-icon-selection-symbol-for-interface-of-a-square-of-broken-line-32454.png"),
                        transform=Transform(scale=Vector2(1, 1)),
                        layer=1,
                        name="attack pokemon frame image stable")
                    draw_check_frame(position=collider_image_attack.rect.center, ui=self.ui,
                                     pokemons=self.chosen_pokemons,
                                     frame_image=image)
                    self.attack_button.color = colors.GREEN
                    self.attack_button.interactive = True
            if collider_image_defensive:
                if self.defensive_pokemon is None:
                    previous_defensive = None
                else:
                    previous_defensive = self.convert_image_to_pokemon([self.defensive_pokemon], self.second_trainer.dict_box, True)[0]
                if self.defensive_pokemon:
                    self.ui.remove_UI_element("defensive pokemon frame image stable")
                    self.defensive_pokemon = None
                if previous_defensive != collider_image_defensive:
                    self.defensive_pokemon = self.second_trainer.dict_box[collider_image_defensive]
                    image = Image(image=pygame.image.load(
                        "../images/UI/free-icon-selection-symbol-for-interface-of-a-square-of-broken-line-32454.png"),
                        transform=Transform(scale=Vector2(1, 1)),
                        layer=1,
                        name="defensive pokemon frame image stable")
                    draw_check_frame(position=collider_image_defensive.rect.center, ui=self.ui,
                                     pokemons=list(self.second_trainer.dict_box.values()),
                                     frame_image=image)
            if self.defensive_pokemon and self.attack_pokemon:
                self.attack_button.color = colors.GREEN
                self.attack_button.interactive = True
            else:
                self.attack_button.color = colors.RED
                self.attack_button.interactive = False

    def convert_image_to_pokemon(self, image: list[Image] | list[Pokemon], source: dict, revers: bool = False) -> list[
                                                                                                                      Pokemon] | \
                                                                                                                  list[
                                                                                                                      Image]:
        pokemons = []
        if revers:
            for i in image:
                pokemons.append(list(source.keys())[list(source.values()).index(i)])
        else:
            for i in image:
                pokemons.append(source[i])
        return pokemons

    def start_battle(self):
        self.ui.remove_UI_element("pokemon image")
        self.ui.remove_UI_element("start fight button")
        self.ui.remove_UI_element("frame image stable")
        self.ui.remove_UI_element("choose pokemons text")
        self.battle_status = BattleScene.BattleState.CHOICE
        print("START BATTLE COMPLETE")
        self.draw_pokemons_in_row((100, 100), self.convert_image_to_pokemon(self.chosen_pokemons, self.image_list))
        self.generate_second_trainer()
        self.draw_pokemons_in_row((600, 100), list(self.second_trainer.dict_box.values()), True)
        self.attack_text = Text("Выберите атакующего и цель", colors.WHITE,
                                Transform(position=(self.game_data.resolution[0] // 2, 50, 0)),
                                300, 50)
        self.attack_button: Button = Button(color=colors.DARK_GRAY, width=0,
                                            text=Text("Attack!", (255, 255, 255)),
                                            button_event=self.attack,
                                            transform=Transform(position=Vector2(400,
                                                                                 400),
                                                                scale=Vector2(1, 1)),
                                            height=60, length=200, name="attack button",
                                            interactive=False)
        self.ui.add_new_UI_element([self.attack_text, self.attack_button])

    def generate_second_trainer(self):
        self.second_trainer = Trainer(Transform(), Surface((0, 0)), 0)
        general_pokemon_width = 60
        general_pokemon_height = 60
        for _ in range(config.battle_team_size):
            pokemon_type = random.choice(list(Pokemon.PokemonType)).name
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
            if pokemon_type == Pokemon.PokemonType.water.name:
                self.second_trainer.add(WaterPokemon(name="wp",
                                                     transform=Transform(),
                                                     image=image,
                                                     atk=random.randint(1, Pokemon.max_pokemon_atk),
                                                     df=random.randint(1, Pokemon.max_pokemon_df)), True)
            elif pokemon_type == Pokemon.PokemonType.fire.name:
                self.second_trainer.add(FirePokemon(name="fp", transform=Transform(),
                                                    image=image,
                                                    atk=random.randint(1, Pokemon.max_pokemon_atk),
                                                    df=random.randint(1, Pokemon.max_pokemon_df)), True)
            elif pokemon_type == Pokemon.PokemonType.grass.name:
                self.second_trainer.add(GrassPokemon(name="gp", transform=Transform(),
                                                     image=image,
                                                     atk=random.randint(1, Pokemon.max_pokemon_atk),
                                                     df=random.randint(1, Pokemon.max_pokemon_df)), True)
            else:
                self.second_trainer.add(ElectricPokemon(name="ep", transform=Transform(),
                                                        image=image,
                                                        atk=random.randint(1, Pokemon.max_pokemon_atk),
                                                        df=random.randint(1, Pokemon.max_pokemon_df)), True)

    @Scene.start_decorator
    def start(self):
        first_pokemon_position = Vector2(330, 130)
        image_list, size, center = choice_team(player_team=self.player.box,
                                               first_pokemon_position=first_pokemon_position,
                                               pokemons_in_row=5,
                                               pixel_size=(100, 100))
        self.image_list = image_list
        print(size, center, [i.name for i in image_list])
        # self.ui.add_new_UI_element(Rect(transform=Transform(position=center, scale=Vector2(1, 1)),
        #                                 width=int(size.x), height=int(size.y), color=(255, 0, 0),
        #                                 name="choice pokemon bg"))
        self.ui.add_new_UI_element(list(image_list.keys()))
        self.ui.add_new_UI_element(Text(text=f"Выберите {config.battle_team_size} покемонов для боя", height=40,
                                        width=100, text_color=colors.WHITE,
                                        transform=Transform(position=Vector2(self.game_data.resolution[0] // 2, 20)),
                                        name="choose pokemons text"))

    def draw_pokemons_in_row(self, start_pos, pokemons: list[Pokemon], isTrain: bool = False):
        # if isTrain:
        #     self.second_trainer.dict_box.clear()
        shift_y = 40
        shift_x = 20
        max_in_col = (self.game_data.resolution[1] - start_pos[1] - shift_y) // (pokemons[0].rect.height + shift_y)
        print("MC", max_in_col, self.game_data.resolution[1] - start_pos[1], pokemons[0].rect.height + shift_y)
        for pokemon in range(len(pokemons)):
            pokemons[pokemon].rect.center = (
                    start_pos + Vector2((self.chosen_pokemons[pokemon].rect.width + shift_x) * (pokemon // max_in_col),
                                        (self.chosen_pokemons[pokemon].rect.height + shift_y) * (pokemon % max_in_col)))
            pokemon_rect = pokemons[pokemon].rect
            common_distance = pokemon_rect.width
            img = pygame.image.load("../images/UI/sword.png")
            text_size = (20, 20)
            damage = pokemons[pokemon].get_atk()
            hp = pokemons[pokemon].get_hp()
            df = pokemons[pokemon].get_def()
            scale = (0.1, 0.1)
            pixel_size = (20, 20)
            sword_image = Image(transform=Transform(Vector2(pokemon_rect.left,
                                                            pokemon_rect.center[1] + pokemon_rect.height // 2 +
                                                            pixel_size[1] // 2),
                                                    Vector2(scale)),
                                image=img, pixel_size=pixel_size)
            sword_text = Text(text=str(damage), height=text_size[1],
                              width=text_size[0], text_color=colors.WHITE,
                              transform=Transform(Vector2(sword_image.rect.center[0],
                                                          pokemon_rect.center[1] + pokemon_rect.height // 2 +
                                                          pixel_size[1] // 2 + pixel_size[1]),
                                                  Vector2(scale)), name="sword data text")
            img = pygame.image.load("../images/UI/shield.png")
            shield_image = Image(transform=Transform(Vector2(pokemon_rect.center[0] + common_distance // 3,
                                                             pokemon_rect.center[1] + pokemon_rect.height // 2 +
                                                             pixel_size[1] // 2),
                                                     Vector2(scale)),
                                 image=img, pixel_size=pixel_size)
            shield_text = Text(text=str(df), height=text_size[1],
                               width=text_size[0], text_color=colors.WHITE,
                               transform=Transform(Vector2(shield_image.rect.center[0],
                                                           pokemon_rect.center[1] + pokemon_rect.height // 2 +
                                                           pixel_size[1] // 2 + pixel_size[1]),
                                                   Vector2(scale)), name="shield data text")
            img = pygame.image.load("../images/UI/shield2.png")
            hp_image = Image(transform=Transform(Vector2(pokemon_rect.left + common_distance // 3 * 2,
                                                         pokemon_rect.center[1] + pokemon_rect.height // 2 +
                                                         pixel_size[1] // 2),
                                                 Vector2(scale)),
                             image=img, pixel_size=pixel_size)
            hp_text = Text(text=str(hp), height=text_size[1],
                           width=text_size[0], text_color=colors.WHITE,
                           transform=Transform(Vector2(hp_image.rect.center[0],
                                                       pokemon_rect.center[1] + pokemon_rect.height // 2 +
                                                       pixel_size[1] // 2 + pixel_size[1]),
                                               Vector2(scale)), name="hp data text")
            print("L", self.chosen_pokemons[pokemon].rect)
            # image = Image(Transform(pokemon_rect), pokemons[pokemon].get_img(), rect=pokemon_rect)
            if isTrain:
                necessary_image = list(self.second_trainer.dict_box.keys())[(list(self.second_trainer.dict_box.values()).index(pokemons[pokemon]))]
                # print("TRAIN")
                # self.second_trainer.dict_box[necessary_image] = pokemons[pokemon]
            else:
                necessary_image = list(self.image_list.keys())[
                    (list(self.image_list.values()).index(pokemons[pokemon]))]
            necessary_image.image = pokemons[pokemon].get_img()
            necessary_image.rect = pokemon_rect
            self.ui.add_new_UI_element(
                [necessary_image, sword_image, shield_image, sword_text, shield_text, hp_image, hp_text])
        if isTrain:
            print("KEYS", self.second_trainer.dict_box.keys())

    @Scene.main_loop_decorator
    def main_loop(self):
        for pokemon in list(self.image_list.values()):
            if pokemon.hp_text:
                pokemon.hp_text.text = pokemon.get_hp()

    def check_alive(self, is_attack: bool):
        if is_attack:
            if self.attack_pokemon.get_hp() <= 0:
                self.ui.remove_UI_element(self.convert_image_to_pokemon([self.attack_pokemon], self.image_list, True)[0])
                self.chosen_pokemons.remove(self.convert_image_to_pokemon([self.attack_pokemon], self.image_list, True)[0])
                self.attack_pokemon = None
        else:
            if self.defensive_pokemon.get_hp() <= 0:
                self.ui.remove_UI_element(self.convert_image_to_pokemon([self.defensive_pokemon], self.second_trainer.dict_box, True)[0])
                self.second_trainer.dict_box.pop(self.convert_image_to_pokemon([self.defensive_pokemon], self.second_trainer.dict_box, True)[0])
                self.defensive_pokemon = None
