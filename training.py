import tensorflow.keras as keras
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Nadam,Adam
import tensorflow as tf
import numpy as np
from timeit import default_timer as timer
import play
import mcts_agent
import connect4

tf.autograph.set_verbosity(3)

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
  model.add(keras.layers.Dense(42, activation='relu', input_shape=(42,)))
  model.add(BatchNormalization())
  model.add(Dropout(0.1))
  model.add(keras.layers.Dense(512, activation='relu'))
  model.add(BatchNormalization())
  model.add(Dropout(0.2))
  model.add(keras.layers.Dense(42, activation='relu'))
  model.add(BatchNormalization())
  model.add(Dropout(0.1))
  model.add(keras.layers.Dense(7,  activation='softmax'))
  model.compile(loss='categorical_crossentropy', optimizer="adam", metrics=['accuracy'])
  return model


def train_model(model, X, Y):
  X = np.array(X)
  Y = np.array(Y)
  model.fit(X, Y, epochs=epochs)
 # model.fit(X, Y, epochs=epochs)

def train():
  def to_training_data(game, result, agentname):
    X = []
    Y = []
    draws = result[3]
    if result[0][0] == agentname:
      outcome = result[2]
      agent = 0
    elif result[0][1] == agentname:
      outcome = -result[2]
      agent = 1
    else:
      print('Oops, agent not playing!')
      return X, Y
    game.setup()
    for i, return_value in enumerate(result[1]):
      move, value, max_i, moves, policy, q = return_value
      if i % 2 == agent:
        X.append(game.get_board().flatten())
        Y.append(output_represention(moves, policy))
      game.drop_piece_in_column(move)
    return np.array(X), np.array(Y)


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

 # X = []
 # Y = []
  global model
  while True:
    X = []
    Y = []
    results = training_games(agents, 10)
    for result in results:
      x, y = to_training_data(game, result, agents[0].name())
      X.extend(x)
      Y.extend(y)
    train_model(model, np.array(X), np.array(Y))
    model.save('model_final_updated.h5')
    print('model saved!')

game = connect4.Connect4()
model = None
model = create_model()
model.save('model_final_updated.h5')
agent1_param = {'name':'mc_AZ', 'advanced': True, 'simulations': 150, 'explore': 5, 'model': model}
agent2_param = {'name':'mc_standard', 'simulations':250, 'explore': 5}
agents = [mcts_agent.MCTSAgent(agent1_param), mcts_agent.MCTSAgent(agent2_param)]
agents_eval = agents

train()