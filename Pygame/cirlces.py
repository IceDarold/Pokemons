import math
import random

import pygame
from Lessons.Pokemons import colors

is_running = True
SIZE = (1920, 1080)
FPS = 60
pygame.init()
screen = pygame.display.set_mode(SIZE)
r = 0
clock = pygame.time.Clock()
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
    screen.fill(color=colors.BLACK)
    count = 100
    if math.sin(r) >= 0 and math.sin(r) - 0.01 <= 0 or math.sin(r) - 0.01 <= -1:
        new_position = [(random.randint(r//1, SIZE[0] - r // 1), random.randint(r//1, SIZE[1] - r//1)) for i in range(count)]
        colors_list = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                        ) for i in range(count)]
        sizes = [random.randint(0, 10) for i in range(count)]
    for i in range(count):
        new_position[i] = (new_position[i][0] + random.randint(-10, 10), new_position[i][1] + random.randint(-40, 40))
    for i in range(count):
        pygame.draw.circle(screen, colors_list[i], new_position[i], math.sin(r) * 100 + 100,  sizes[i])
    clock.tick(FPS)
    r += math.sin(pygame.time.get_ticks() / 1000) * 0.05
    print(pygame.time.get_ticks() / 1000)
    pygame.display.flip()
