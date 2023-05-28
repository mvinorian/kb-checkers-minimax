import pygame
from .board import Board
from .constants import RED, WHITE, HELPER, SQUARE

arr = []

class Game:
    HELPER_SIZE = 15

    # Inisialisasi game
    def __init__(self, window: pygame.Surface):
        self.selected = None
        self.board = Board()
        self.window = window
        self.turn = RED
        self.valid_moves = {}
        self.is_tie = False

    # Pembaharuan tampilan game
    def update(self):
        self.board.draw(self.window)
        self.draw_valid_moves()
        pygame.display.update()

    # Pemilihan bidak yang akan dijalankan
    def select(self, position: tuple):
        if self.selected:
            if position in self.valid_moves:
                self.board.move(self.selected, position)
                eaten = self.valid_moves[position]
                if eaten:
                    self.board.remove(eaten)
                self.change_turn()
                arr.append(position)
                if len(arr) > 2:
                    if arr[len(arr) - 3] != arr[len(arr) - 1]:
                        arr.clear()
                        arr.append(position)
                        
                if len(arr) == 5:
                    self.is_tie = True
            else:
                self.selected = None
                self.valid_moves = {}
                self.select(position)

        piece = self.board.get_piece(position)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    # Mengganti giliran
    def change_turn(self):
        self.valid_moves = {}
        self.turn = WHITE if self.turn == RED else RED

    # Menggambarkan gerak yang memungkinkan untuk bidak yang sebelumnya di pilih (select)
    def draw_valid_moves(self):
        for move in self.valid_moves:
            row, col = move
            pygame.draw.circle(self.window, HELPER, (col*SQUARE+SQUARE//2, row*SQUARE+SQUARE//2), self.HELPER_SIZE)

    # Mengembalikan siapa pemenang game
    def winner(self):
        return self.board.winner()

    # Mengembalikan nilai seri
    def tie(self):
        return self.board.tie(self.is_tie)

    # Fungsi untuk melakukan transisi menuju giliran oposisi dari agent
    def agent_move(self, board: Board):
        self.board = board
        self.change_turn()
