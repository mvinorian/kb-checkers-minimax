import pygame, sys, time
from checkers.game import Game
from checkers.constants import WIDTH, HEIGHT, SQUARE, WHITE
from checkers.algorithm import alphabeta
from ui.button import Button

pygame.init()
FPS = 60

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers | Alphabeta')

# Mengembalikan posisi
def get_row_col(position):
    x, y = position
    row = y//SQUARE
    col = x//SQUARE
    return row, col

# Mengembalikan jenis font yang dibutuhkan
def get_font(size: int):
    return pygame.font.Font("assets/bloomberg.otf", size)

# Menampilkan hasil akhir
def win_state(winner: str):
    while True:
        WINDOW.fill("Black")
        state_mouse_pos = pygame.mouse.get_pos()
        if winner == "GAME TIE":
            state_text = get_font(100).render(winner, True, "white")
        else:    
            state_text = get_font(100).render(winner +" Win", True, winner)
        state_box = state_text.get_rect(center=(200, 100))

        WINDOW.blit(state_text, state_box)

        back_button = Button(x_pos=200, y_pos=400, text_show="Back To Menu", font=get_font(65), base_color="white", hovering_color="#FF0000")
        back_button.hoverColor(state_mouse_pos)
        back_button.update(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkMouseInput(state_mouse_pos):
                    main()

        pygame.display.update()

# Fungsi utama yang menjalankan dan menampilkan jalannya game 
def play():
    running = True
    clock = pygame.time.Clock()
    game = Game(WINDOW)

    while running:
        clock.tick(FPS)
        game.update()

        if game.winner() != None:
            print(game.winner() + ' WIN!')
            running = False
            win_state(game.winner())

        if game.tie() != None:
            print('GAME TIE!')
            running = False
            win_state(game.tie())

        if game.turn == WHITE:
            start = time.time()
            _, best_board = alphabeta(game.board, 5, game)
            end = time.time()
            game.agent_move(best_board)
            print(f"time: {end - start}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = get_row_col(pygame.mouse.get_pos())
                game.select(position)

# Fungsi untuk menampilkan main menu
def main():
    
    while True:
        WINDOW.fill("white")

        main_mouse_pos = pygame.mouse.get_pos()

        main_text = get_font(100).render("Checkers", True, "#1c1c1c")
        main_box = main_text.get_rect(center=(200, 150))

        WINDOW.blit(main_text, main_box)
        
        play_button = Button(x_pos=200, y_pos=400, text_show="PLAY", font=get_font(65), base_color="black", hovering_color="#FF0000")
        quit_button = Button(x_pos=200, y_pos=500, text_show="Quit", font=get_font(65), base_color="black", hovering_color="#FF0000")

        for button in [play_button, quit_button]:
            button.hoverColor(main_mouse_pos)
            button.update(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkMouseInput(main_mouse_pos):
                    play()
                if quit_button.checkMouseInput(main_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == '__main__':
    main()
