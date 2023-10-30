import os

import pygame
from magic_filter.operations import function
from pygame import Surface, Vector3
from pygame.event import Event

import Pokemons.main_files.Pokemon
from Pokemons.Base_classes import config
from Pokemons.Base_classes.Camera import Camera
from Pokemons.Base_classes.game_object import GameObject
from Pokemons.Base_classes.transform import Transform
from Pokemons.Scenes.hunting_scene.maze_cell import MazeCell
from Pokemons.animation_system.animation import Animation
from Pokemons.main_files.trainer import Trainer


class Player(Trainer):
    def __init__(self, transform: Transform = Transform(), hunting_turn_number: int = 0, move_through_ring: bool = False,
                 resolution: tuple[int, int] = None):
        # Номер игрока в очереди за охотой на покемонов
        self.hunting_turn_number = hunting_turn_number
        idle_image = pygame.image.load("../images/Trainers_animations/First trainer/Go_backward/1.png")
        idle_image.set_colorkey((255, 255, 255))
        print(idle_image.get_size(), "PLAYER")
        self._transform = transform
        self._player_real_pos = Vector3(300, 200, 0)
        _transform = transform.copy()
        _transform.position = self._player_real_pos
        super().__init__(_transform, speed=config.player_speed_normal, image=idle_image, move_through_ring=move_through_ring, resolution=resolution)
        self._last_keys = pygame.key.get_pressed()
        self.collider_enter_actions: list[function] = []
        self.animations: dict[str, Animation] = {}
        self._first_frame = True
        self.load_animations()

    def load_animations(self):
        update_period = 1 / (self._speed * 2)
        forward_anim_list = os.listdir("../images/Trainers_animations/First trainer/Go_forward")
        forward_animation = []
        for i in forward_anim_list:
            image = pygame.image.load("../images/Trainers_animations/First trainer/Go_forward/" + i)
            image.set_colorkey((255, 255, 255))
            forward_animation.append(image)
        right_anim_list = os.listdir("../images/Trainers_animations/First trainer/Go_right")
        right_animation = []
        for i in right_anim_list:
            image = pygame.image.load("../images/Trainers_animations/First trainer/Go_right/" + i)
            image.set_colorkey((255, 255, 255))
            right_animation.append(image)
        backward_anim_list = os.listdir("../images/Trainers_animations/First trainer/Go_backward")
        backward_animation = []
        for i in backward_anim_list:
            image = pygame.image.load("../images/Trainers_animations/First trainer/Go_backward/" + i)
            image.set_colorkey((255, 255, 255))
            backward_animation.append(image)
        left_anim_list = os.listdir("../images/Trainers_animations/First trainer/Go_leftward")
        left_animation = []
        for i in left_anim_list:
            image = pygame.image.load("../images/Trainers_animations/First trainer/Go_leftward/" + i)
            image.set_colorkey((255, 255, 255))
            left_animation.append(image)
        item_animation = [pygame.image.load("../images/Trainers_animations/First trainer/Go_backward/1.png")]
        item_animation[0].set_colorkey((255, 255, 255))
        self.animations = {
            "Forward": Animation(forward_animation, update_period, self.transform),
            "Right": Animation(right_animation, update_period, self.transform),
            "Backward": Animation(backward_animation, update_period, self.transform),
            "Left": Animation(left_animation, update_period, self.transform),
            "Item": Animation(item_animation, update_period, self.transform)
        }

    def collider_enter(self, game_object):
        for action in self.collider_enter_actions:
            action(game_object)
        if isinstance(game_object, Pokemons.main_files.pokemons.Pokemon):
            self.add(game_object)
            GameObject.all_objects.remove(game_object)

    def actions(self, e: Event):
        if e.type == pygame.KEYDOWN:
            self.sprint = e.mod == pygame.K_LSHIFT
            print(e.mod, pygame)
            self._last_keys = pygame.key.get_pressed()
            if self._last_keys[pygame.K_w] and self._move_direction.y > -1:
                self._move_direction.y += -1
            if self._last_keys[pygame.K_s] and self._move_direction.y < 1:
                self._move_direction.y += 1
            if self._last_keys[pygame.K_a] and self._move_direction.x > -1:
                self._move_direction.x += -1
            if self._last_keys[pygame.K_d] and self._move_direction.x < 1:
                self._move_direction.x += 1
        if e.type == pygame.KEYUP:
            self.sprint = e.mod == pygame.K_LSHIFT
            current_keys = pygame.key.get_pressed()
            if self._last_keys[pygame.K_w] and not current_keys[pygame.K_w]:
                self._move_direction.y -= -1
            if self._last_keys[pygame.K_s] and not current_keys[pygame.K_s]:
                self._move_direction.y -= 1
            if self._last_keys[pygame.K_a] and not current_keys[pygame.K_a]:
                self._move_direction.x -= -1
            if self._last_keys[pygame.K_d] and not current_keys[pygame.K_d]:
                self._move_direction.x -= 1
            self._last_keys = current_keys

    def draw(self, surface: Surface):
        if self._first_frame:
            Camera.move_camera(-self._transform.position.xy, [self])
            # self.transform.position = self.player_real_pos
            self._first_frame = False
        if self._move_direction.y == -1:
            self.animations["Forward"].draw(surface)
        elif self._move_direction.y == 1:
            self.animations["Backward"].draw(surface)
        elif self._move_direction.x == -1:
            self.animations["Left"].draw(surface)
        elif self._move_direction.x == 1:
            self.animations["Right"].draw(surface)
        else:
            self.animations["Item"].draw(surface)
