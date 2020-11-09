import utils
import copy

def play_a_game(game, A, time):
    game.setup()
    board_history = []
    # if output:
    #     print(game)
    n = 0
    A[0].reset()
    A[1].reset()
    while not game.is_terminal_node():
        value, column = A[n % 2].play(copy.deepcopy(game), utils.CheckAbort(time))
        game.drop_piece_in_column(column)
        board_history.append(game.get_board())
        n += 1
    result = 0
    if game.winning_move():
        if game.get_to_move() == game.PLAYER_1:
            result = -1
        else:
            result = 1
    return board_history, result

def play_a_match(game, agents, num_games, time):
    all_games_history = []
    all_games_result = []
    for _ in range(num_games):
        board_history, result = play_a_game(game, agents, time)
        all_games_history.append(board_history)
        all_games_result.append(result)
        board_history, result = play_a_game(game, agents[::-1], time)
        all_games_history.append(board_history)
        all_games_result.append(result)
    return all_games_history, all_games_result

