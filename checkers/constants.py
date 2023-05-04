import pygame

SQUARE = 100
ROWS, COLS = 6, 4
WIDTH, HEIGHT = SQUARE * COLS, SQUARE * ROWS

BG_DARK = (106, 155, 65)
BG_LIGHT = (200, 200, 200)
RED = (230, 26, 35)
WHITE = (255, 255, 255)
HELPER = (30, 30, 30)
OUTLINE = (100, 100, 100)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))
