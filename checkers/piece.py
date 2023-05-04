import pygame
from .constants import SQUARE, OUTLINE, CROWN


class Piece:
    PADDING = 10

    def __init__(self, position: tuple, color):
        self.row, self.col = position
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.update()

    def update(self):
        self.x = self.col*SQUARE + SQUARE//2
        self.y = self.row*SQUARE + SQUARE//2

    def draw(self, window: pygame.Surface):
        radius = SQUARE//2 - self.PADDING
        pygame.draw.circle(window, OUTLINE, (self.x, self.y), radius + 1)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)
        if self.king:
            window.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    def move(self, position: tuple):
        self.row, self.col = position
        self.update()

    def promote(self):
        self.king = True
