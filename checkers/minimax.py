from .game import Game
from .board import Board
from .piece import Piece
from .constants import RED, WHITE
from copy import deepcopy


def minimax(board: Board, depth: int, is_max: bool, game: Game) -> list:
    if depth == 0 or board.winner() != None:
        return [board.evaluate(), board]

    if is_max:
        max_eval = float('-inf')
        best_move = None

        for move in get_all_moves(board, WHITE, game):
            evaluation = minimax(move, depth-1, False, game)[0]
            max_eval = max(evaluation, max_eval)
            if evaluation == max_eval:
                best_move = move
            
        return [max_eval, best_move]

    min_eval = float('inf')
    best_move = None
    
    for move in get_all_moves(board, RED, game):
        evaluation = minimax(move, depth-1, True, game)[0]
        min_eval = min(evaluation, min_eval)
        if evaluation == min_eval:
            best_move = move

    return [min_eval, best_move]

def simulate_move(piece: Piece, position: tuple, board: Board, eaten: list) -> Board:
    board.move(piece, position)
    if eaten:
        board.remove(eaten)

    return board

def get_all_moves(board: Board, color: tuple, game: Game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)

        for position, eaten in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece((piece.row, piece.col))
            new_board = simulate_move(temp_piece, position, temp_board, eaten)
            moves.append(new_board)

    return moves
            