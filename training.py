import tensorflow.keras as keras

import numpy as np
from timeit import default_timer as timer
import play
import mcts_agent
import connect4

numberOfInputs = 42
numberOfOutputs = 7
batchSize = 50
epochs = 100

def output_represention(moves, policy):
  tensor = np.zeros(7)
  for i, p in enumerate(policy):
    tensor[moves[i]] = p
  return tensor

def create_model():
  model = keras.Sequential()
  model.add(keras.layers.Dense(42, activation='relu', input_shape=(6,7)))
  model.add(keras.layers.Dense(42, activation='relu'))
  model.add(keras.layers.Dense(numberOfOutputs, activation='softmax'))
  model.compile(loss='categorical_crossentropy', optimizer="rmsprop", metrics=['accuracy'])
  return model


def train_model(model, X, Y):
  X = np.array(X)
  Y = np.array(Y)
  model.fit(X, Y, epochs=20)

def train():
  def to_training_data(game, result, agentname):
    X = []
    Y = []
    draws = result[4]
    if result[0][0] == agentname:
      outcome = result[3]
      agent = 0
    elif result[0][1] == agentname:
      outcome = -result[3]
      agent = 1
    else:
      print('Oops, agent not playing!')
      return X, Y
    game.setup()
    for i, return_value in enumerate(result[2]):
      move, value, max_i, moves, policy, q = return_value
      if i % 2 == agent:
        X.append(game.get_board())
        Y.append(output_represention(moves, policy))
      game.make(move)
    return X, Y


  def training_games(agents, num_games):
    # global model_evaluator
    # model.save('model.h5')
    # model_evaluator = load_model('model.h5',compile=False)
    start_time = timer()
    game_records = play.play_a_match(game, agents, num_games, 0)
    print("Time:", timer() - start_time)
    print('Match result')
    score_color, score_agent, draws = play.score_game_records(game_records, agents)
    print(score_color)
    print(score_agent)
    print('Draws: %d' % (draws))
    return game_records

  X = []
  Y = []
  global model
  for _ in range(1, 3):
    results = training_games(agents, 5)
    for result in results:
      x, y = to_training_data(game, result, agents[0].name())
      X.extend(x)
      Y.extend(y)
    train_model(model, X, Y)
  print('hi')
  return

game = connect4.Connect4()
model = None
model = create_model()
agent1_param = {'name':'mc_AZ', 'simulations':250, 'explore': 8, 'model': model}
agent2_param = {'name':'mc_standard', 'advanced': True, 'simulations':250, 'explore': 8}
agents = [mcts_agent.MCTSAgent(agent1_param), mcts_agent.MCTSAgent(agent2_param)]
agents_eval = agents

train()