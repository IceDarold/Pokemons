import math
import time

import pygame

from Lessons.Pokemons import colors

mm = pygame.image.load("unnamed.png")
#Задаем положение по центру
start_point = pygame.Vector2(900, 500)
position = pygame.Vector2(start_point)
mm_rect = mm.get_rect(center=position)
is_running = True
SIZE = (1000, 1500)
FPS = 60
pygame.init()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
print(position.x, position.y)
speed = pygame.Vector2(2, 2)
mm = pygame.transform.scale(mm, (mm.get_width() // 1, mm.get_height() // 1))
r = 100
while is_running:
    start_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
    mm_rect = mm.get_rect(center=position)
    screen.fill(color=colors.BLACK)
    screen.blit(mm, mm_rect)
    # pygame.draw.circle(radius=math.cos(pygame.time.get_ticks() * 0.001) * math.sin(pygame.time.get_ticks() * 0.01) * 0 + 100, center=position, color=colors.WHITE, surface=screen)
    vector = (30 * math.tan(pygame.time.get_ticks() * 0.001) * math.cos(pygame.time.get_ticks() * 0.001) * math.sin(pygame.time.get_ticks() * 0.01),
    30 * (math.sin(pygame.time.get_ticks() * 0.001) * math.cos(pygame.time.get_ticks() * 0.01)))
    print(FPS, 1 / (time.time() - start_time))
    position += (vector[0], vector[1])
    r += 0.05 * math.cos(pygame.time.get_ticks() * 0.001) * math.sin(pygame.time.get_ticks() * 0.01)
    clock.tick(FPS)
    pygame.display.flip()
