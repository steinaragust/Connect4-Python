import math
import random

def evaluate_window(game, window):
    score = 0
    piece = game.get_piece()
    opp_piece = game.get_opponent_piece()

    if window.count(opp_piece) == 4:
        score += 100
    elif window.count(opp_piece) == 3 and window.count(game.EMPTY) == 1:
        score += 5
    elif window.count(opp_piece) == 2 and window.count(game.EMPTY) == 2:
        score += 2

    if window.count(piece) == 3 and window.count(game.EMPTY) == 1:
        score -= 4

    return score


def score_position(game):
    score = 0
    board = game.get_board()
    ## Score center column
    center_array = [int(i) for i in list(board[:, game.COLUMN_COUNT // 2])]
    center_count = center_array.count(game.get_opponent_piece())
    score += center_count * 3

    turn = game.get_to_move()

    ## Score Horizontal
    for r in range(game.ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(game.COLUMN_COUNT - 3):
            window = row_array[c: c + game.WINDOW_LENGTH]
            score += evaluate_window(window)

    ## Score Vertical
    for c in range(game.COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(game.ROW_COUNT - 3):
            window = col_array[r: r + game.WINDOW_LENGTH]
            score += evaluate_window(window)

    ## Score posive sloped diagonal
    for r in range(game.ROW_COUNT - 3):
        for c in range(game.COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(game.WINDOW_LENGTH)]
            score += evaluate_window(window)

    for r in range(game.ROW_COUNT - 3):
        for c in range(game.COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(game.WINDOW_LENGTH)]
            score += evaluate_window(window)

    return -score if turn == game.PLAYER_1 else score

def alphabeta(game, depth, alpha, beta, check_abort):
    valid_locations = game.get_valid_locations()
    is_terminal = game.is_terminal_node()
    turn = game.get_to_move()
    if is_terminal:
        if game.winning_move():
            return None, (-1 if turn == game.PLAYER1 else 1) * 100000000000000, False
        else:  # Game is over, no more valid moves
            return None, 0, False
    if depth == 0:
        return None, score_position(game), False
    if check_abort.do_abort():
        return None, 0, True

    value = -math.inf if turn == game.PLAYER1 else math.inf
    column = random.choice(valid_locations)

    do_abort = False
    for col in valid_locations:
        row = game.get_next_open_row(col)
        piece = game.get_piece()
        game.drop_piece(row, col, piece)
        _, new_score, do_abort = alphabeta(game, depth - 1, alpha, beta)
        game.retract_piece(row, col)
        if do_abort:
            break
        if (turn == game.PLAYER1 and new_score > value) or (turn == game.PLAYER2 and new_score < value):
            value = new_score
            column = col
        if turn == game.PLAYER1:
            alpha = max(alpha, value)
        else:
            beta = min(beta, value)
        if alpha >= beta:
            break
    return column, value, do_abort

def id_alphabeta(game, check_abort, params):
    do_abort = False
    best_column = 0
    best_value = 0
    max_depth = 5
    depth = 1

    while not do_abort:
        column, value, do_abort = alphabeta(game, depth, -math.inf, math.inf, check_abort)
        if not do_abort:
            best_column = column
            best_value = value
        depth += 1
        if max_depth > 0 and depth == max_depth:
            break
    return best_value, best_column
