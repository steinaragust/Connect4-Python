import utils
import copy

def play_a_game(game, A, time):
    game.setup()
    return_values = []
    # if output:
    #     print(game)
    n = 0
    A[0].reset()
    A[1].reset()
    while not game.is_terminal_node():
        print('starting move for: ', A[n % 2].name())
        move, value, max_i, moves, policy, q = A[n % 2].play(copy.deepcopy(game), utils.CheckAbort(time))
        print('end move')
        return_values.append((move, value, max_i, moves, policy, q))
        game.drop_piece_in_column(move)
        n += 1
    result = 0
    draws = 0
    if game.winning_move():
        if game.get_to_move() == game.PLAYER_1:
            result = -1
        else:
            result = 1
    else:
        draws += 1
    return [A[0].name(), A[1].name()], return_values, result, draws

def play_a_match(game, agents, num_games, time):
    game_records = []
    for _ in range(num_games):
        game_record = play_a_game(game, agents, time)
        game_records.append(game_record)
        game_record = play_a_game(game, agents[::-1], time)
        game_records.append(game_record)
        score_game_records(game_records, agents)
    print('match over')
    return game_records


def score_game_records(game_records, agents):
    score_color = {'Player1': 0, 'Player2': 0}
    score_agent = {agents[0].name(): 0, agents[1].name(): 0}
    draws = 0
    for record in game_records:
        if record[1] == 1:
            score_color['Player1'] += 1
            score_agent[record[0][0]] += 1
        elif record[1] == -1:
            score_color['Player2'] += 1
            score_agent[record[0][1]] += 1
        else:
            draws += 1
    return score_color, score_agent, draws

