import random

import pygame

WIDTH = 1280  # ширина игрового окна
HEIGHT = 720 # высота игрового окна
FPS = 1 # частота кадров в секунду

COLOR = {
    "BLACK": (0, 0, 0),
    "WHITE": (55, 255, 255),
    "RED": (55, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
}
pygame.init()
screen = pygame.display.set_mode(size=(WIDTH, HEIGHT))
pygame.display.set_caption('My first screen')
clock = pygame.time.Clock()

run = True
while run:
    clock.tick(FPS)
    screen.fill(random.choice(list(COLOR.values())))
    pygame.display.flip()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()

