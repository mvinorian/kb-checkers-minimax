import pygame
from .piece import Piece
from .constants import ROWS, COLS, BG_DARK, BG_LIGHT, SQUARE, RED, WHITE

# Papan permainan Dam (Checkers)
class Board:
    # Inisialisasi papan dan kondisinya
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 4
        self.red_kings = self.white_kings = 0
        self.create_board()

    # Membuat papan
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row == 1:
                    self.board[row].append(Piece((row, col), WHITE))
                elif row == ROWS-2:
                    self.board[row].append(Piece((row, col), RED))
                else:
                    self.board[row].append(0)

    # Visualisasi bentuk papan
    def draw_squares(self, window: pygame.Surface):
        window.fill(BG_DARK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(window, BG_LIGHT, (col*SQUARE, row*SQUARE, SQUARE, SQUARE))

    # Visualisasi bidak 
    def draw(self, window):
        self.draw_squares(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(window)

    # Penghitungan nilai dari papan berdasarkan bidak-bidak yang ada
    def evaluate(self):
        return self.white_left - self.red_left + 0.5 * (self.white_kings - self.red_kings)
    
    # Memberikan pemenang game
    def winner(self):
        if self.red_left <= 0:
            return "WHITE"
        elif self.white_left <= 0:
            return "RED"
        
        return None
    
    # Mendefinisikan seri
    def tie(self, is_tie: bool):
        if is_tie:
            return 'GAME TIE'
        else:
            return None

    # Mendapatkan posisi bidak
    def get_piece(self, position: tuple) -> Piece or int:
        row, col = position
        return self.board[row][col]

    # Mendapatkan seluruh posisi bidak
    def get_all_pieces(self, color: tuple) -> list:
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)

        return pieces

    # Melakukan pembaruan posisi serta karakteristik dari bidak
    def move(self, piece: Piece, position: tuple):
        row, col = position
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(position)

        if row == 0 or row == ROWS -1:
            piece.promote()
            if piece.color == RED:
                self.red_kings += 1
            if piece.color == WHITE:
                self.white_kings += 1

    # Menghapus bidak yang termakan
    def remove(self, pieces: list):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                if piece.color == WHITE:
                    self.white_left -= 1

    # Mendapatkan semua gerak yang memungkinkan
    def get_valid_moves(self, piece: Piece) -> dict:
        moves = {}
        if piece.color == RED or piece.king:
            moves.update(self._traverse_up((piece.row, piece.col), piece.color, piece.king))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_down((piece.row, piece.col), piece.color, piece.king))

        moves.update(self._traverse_left((piece.row, piece.col), piece.color, piece.king))
        moves.update(self._traverse_right((piece.row, piece.col), piece.color, piece.king))

        return moves

    # Mendapatkan gerak atas
    def _traverse_up(self, position: tuple, color: tuple, king: bool, eaten: list = []):
        row, col = position
        moves = {}
        if row-1 < 0:
            return moves

        new_position = (row, col)
        up = self.board[row-1][col]
        up2 = self.board[row-2][col] if row-2 >= 0 else -1

        if up == 0 and not eaten:
            new_position = (row-1, col)
            moves[new_position] = []

        elif up != 0 and up.color != color and up2 == 0:
            new_position = (row-2, col)
            moves[new_position] = eaten + [up]
            moves.update(self._traverse_up(new_position, color, king, eaten=eaten+[up]))
            moves.update(self._traverse_left(new_position, color, king, eaten=eaten+[up]))
            moves.update(self._traverse_right(new_position, color, king, eaten=eaten+[up]))

        return moves

    # Mendapatkan gerak bawah
    def _traverse_down(self, position: tuple, color: tuple, king: bool, eaten: list = []):
        row, col = position
        moves = {}
        if row+1 >= ROWS:
            return moves

        new_position = (row, col)
        down = self.board[row+1][col]
        down2 = self.board[row+2][col] if row+2 < ROWS else -1

        if down == 0 and not eaten:
            new_position = (row+1, col)
            moves[new_position] = []

        elif down != 0 and down.color != color and down2 == 0:
            new_position = (row+2, col)
            moves[new_position] = eaten + [down]
            moves.update(self._traverse_down(new_position, color, king, eaten=eaten+[down]))
            moves.update(self._traverse_left(new_position, color, king, eaten=eaten+[down]))
            moves.update(self._traverse_right(new_position, color, king, eaten=eaten+[down]))

        return moves

    # Mendapatkan gerak kiri
    def _traverse_left(self, position: tuple, color: tuple, king: bool, eaten: list = []):
        row, col = position
        moves = {}
        if col-1 < 0:
            return moves

        new_position = (row, col)
        left = self.board[row][col-1]
        left2 = self.board[row][col-2] if col-2 >= 0 else -1

        if left == 0 and not eaten:
            new_position = (row, col-1)
            moves[new_position] = []

        elif left != 0 and left.color != color and left2 == 0:
            new_position = (row, col-2)
            moves[new_position] = eaten + [left]
            moves.update(self._traverse_left(new_position, color, king, eaten=eaten+[left]))

            if color == RED or king:
                moves.update(self._traverse_up(new_position, color, king, eaten=eaten+[left]))
            if color == WHITE or king:
                moves.update(self._traverse_down(new_position, color, king, eaten=eaten+[left]))

        return moves

    # Mendapatkan gerak kanan
    def _traverse_right(self, position: tuple, color: tuple, king: bool, eaten: list = []):
        row, col = position
        moves = {}
        if col+1 >= COLS:
            return moves

        new_position = (row, col)
        right = self.board[row][col+1]
        right2 = self.board[row][col+2] if col+2 < COLS else -1

        if right == 0 and not eaten:
            new_position = (row, col+1)
            moves[new_position] = []

        elif right != 0 and right.color != color and right2 == 0:
            new_position = (row, col+2)
            moves[new_position] = eaten + [right]
            moves.update(self._traverse_right(new_position, color, king, eaten=eaten+[right]))

            if color == RED or king:
                moves.update(self._traverse_up(new_position, color, king, eaten=eaten+[right]))
            if color == WHITE or king:
                moves.update(self._traverse_down(new_position, color, king, eaten=eaten+[right]))

        return moves
