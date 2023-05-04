import pygame
from checkers.game import Game
from checkers.constants import WIDTH, HEIGHT, SQUARE

FPS = 60

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers Game')

def get_row_col(position):
    x, y = position
    row = y//SQUARE
    col = x//SQUARE
    return row, col

def main():
    running = True
    clock = pygame.time.Clock()
    game = Game(WINDOW)

    while running:
        clock.tick(FPS)
        game.update()

        if game.winner() != None:
            print(game.winner() + ' WIN!')
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = get_row_col(pygame.mouse.get_pos())
                game.select(position)

    pygame.quit()


if __name__ == '__main__':
    main()
