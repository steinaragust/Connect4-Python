from connect4_with_ai_vs_ai import MC_AI, AI, play_game
import connect4
import alphabeta_agent
from timeit import default_timer as timer
import copy
import utils

def play_a_game(game, A):
    game.setup()
    # if output:
    #     print(game)
    n = 0
    A[0].reset()
    A[1].reset()
    while not game.is_terminal():
        column, value = A[n % 2].play(copy.deepcopy(game), utils.CheckAbort(time))
        game.drop_piece_top_column(column)
        n += 1
    if game.get_to_move() == game.PLAYER_1:
        ScorePlayer["Player2"] += 1
        ScoreAgent[A[1].name()] += 1
    else:
        ScorePlayer["Player1"] += 1
        ScoreAgent[A[0].name()] += 1

time = 0.1

games = 5

game = connect4.Connect4()

agents: [alphabeta_agent.AlphaBetaAgent({ "name": "AB1" }), alphabeta_agent.AlphaBetaAgent({ "name": "AB2" })]

ScoreAgent = {agents[0].name(): 0, agents[1].name(): 0}

ScorePlayer = { "Player1": 0, "Player2": 0 }

start_time = timer()

intial_turn = game.PLAYER_1

for _ in range(games):
    play_a_game(game)



