import math
import random
import utils

def alphabeta(game, depth, alpha, beta, maximizingPlayer, check_abort):
    valid_locations = game.get_valid_locations()
    is_terminal = game.is_terminal_node()
    # if is_terminal:
    #     if game.winning_move():
    #         return None, (-1 if maximizingPlayer else 1) * 100000000000000, False
    #     else:  # Game is over, no more valid moves
    #         return None, 0, False
    if depth == 0 or is_terminal:
        score = utils.score_position(game) - depth
        if game.winning_move():
            score = 1000 - depth
        return None, (1 if maximizingPlayer else -1) * score , False
    if check_abort.do_abort():
        return None, 0, True

    value = -math.inf if maximizingPlayer else math.inf
    column = random.choice(valid_locations)

    do_abort = False
    for col in valid_locations:
        game.drop_piece_in_column(col)
        _, new_score, do_abort = alphabeta(game, depth - 1, alpha, beta, not maximizingPlayer, check_abort)
        game.retract_piece_in_column(col)
        if do_abort:
            break
        if (not maximizingPlayer and new_score < value) or (maximizingPlayer and new_score > value):
            value = new_score
            column = col
        if maximizingPlayer:
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
        column, value, do_abort = alphabeta(game, depth, -math.inf, math.inf, True, check_abort)
        if not do_abort:
            if value > best_value:
                best_column = column
                best_value = value
        depth += 1
        if max_depth > 0 and depth == max_depth:
            break
    print(best_value)
    return best_column, best_value
