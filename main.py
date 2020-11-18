from connect4_with_ai_vs_ai import MC_AI, AI, play_game
import connect4
import alphabeta_agent
import mcts_agent
from timeit import default_timer as timer
import copy
import utils
import argparse

def play_a_game(game, A):
    game.setup()
    # if output:
    #     print(game)
    n = 0
    A[0].reset()
    A[1].reset()
    while not game.is_terminal_node():
        values = A[n % 2].play(copy.deepcopy(game), utils.CheckAbort(time))
        game.drop_piece_in_column(values[0])
        #if (A[n % 2].name() == 'AB'):
            #print(game.get_board())
        n += 1
    if game.winning_move():
        if game.get_to_move() == game.PLAYER_1:
            ScorePlayer["Player2"] += 1
            ScoreAgent[A[1].name()] += 1
        else:
            ScorePlayer["Player1"] += 1
            ScoreAgent[A[0].name()] += 1
    else:
        ScorePlayer["Draws"] += 1


ap = argparse.ArgumentParser()
ap.add_argument(
    "-g",
    "--games",
    default=5,
    help="Number of games to play.",
    type=int,
)
ap.add_argument("-t", "--time", default=1, help="Max deliberation time.", type=float)
ap.add_argument(
    "-d",
    "--debug",
    default=False,
    help="Increase output verbosity.",
    action="store_true",
)
ap.add_argument(
    "-i", "--iterdepth", default=0, help="Max iteration-depth for AB.", type=int
)
ap.add_argument(
    "-s", "--simulations", default=0, help="Max number of MCTS simulations.", type=int
)
ap.add_argument(
    "-e",
    "--eval",
    default=False,
    help="Use evaluation function in AB.",
    action="store_true",
)

args = vars(ap.parse_args())
print(args)

time = args['time']

games = args['games']

game = connect4.Connect4()

agent_1_params = {"name": "AB"}
agent_2_params = {"name": "MCTS", 'simulations': 100}

agents = [alphabeta_agent.AlphaBetaAgent(agent_1_params), mcts_agent.MCTSAgent(agent_2_params)]

ScoreAgent = {agents[0].name(): 0, agents[1].name(): 0}

ScorePlayer = {"Player1": 0, "Player2": 0, "Draws": 0}

start_time = timer()

for _ in range(games):
    play_a_game(game, [agents[0], agents[1]])
    play_a_game(game, [agents[1], agents[0]])

time = timer() - start_time
print("Time:", time)
print(ScoreAgent)
print(ScorePlayer)



