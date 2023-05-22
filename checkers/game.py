import pygame
from .board import Board
from .constants import RED, WHITE, HELPER, SQUARE

arr = []

class Game:
    HELPER_SIZE = 15

    def __init__(self, window: pygame.Surface):
        self.selected = None
        self.board = Board()
        self.window = window
        self.turn = RED
        self.valid_moves = {}
        self.is_tie = False

    def update(self):
        self.board.draw(self.window)
        self.draw_valid_moves()
        pygame.display.update()

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

    def change_turn(self):
        self.valid_moves = {}
        self.turn = WHITE if self.turn == RED else RED

    def draw_valid_moves(self):
        for move in self.valid_moves:
            row, col = move
            pygame.draw.circle(self.window, HELPER, (col*SQUARE+SQUARE//2, row*SQUARE+SQUARE//2), self.HELPER_SIZE)

    def winner(self):
        return self.board.winner()

    def tie(self):
        return self.board.tie(self.is_tie)

    def agent_move(self, board: Board):
        self.board = board
        self.change_turn()
