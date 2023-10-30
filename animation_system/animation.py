import time

import pygame
from pygame import Surface

from Pokemons.Base_classes.transform import Transform


class Animation:
    def __init__(self, frames: list[Surface], update_period: float, transform: Transform):
        self.frames = frames
        self.current_frame_index: int = 0
        self.last_update: float = time.time()
        self.update_period = update_period
        self.transform = transform
        print("ANIMATION", transform)
        for frame in frames:
            frames[frames.index(frame)] = pygame.transform.scale(frame, (frame.get_width() * transform.scale.x,
                                                                         frame.get_height() * transform.scale.y))

    def play(self):
        if len(self.frames) == 0:
            print("Количество кадров в анимации равно 0")
            return
        if time.time() - self.last_update >= self.update_period:
            self.last_update = time.time()
            self.current_frame_index += 1
            self.current_frame_index %= len(self.frames)

    def draw(self, surface: Surface):
        self.play()
        rect = self.frames[self.current_frame_index].get_rect()
        rect.center = self.transform.position.xy
        surface.blit(self.frames[self.current_frame_index], rect)
