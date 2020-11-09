from keras import layers
from keras import utils as keras_utils

import numpy as np
from timeit import default_timer as timer
import play
import mcts_agent
import connect4
import utils

numberOfInputs = 42
numberOfOutputs = 3
batchSize = 50
epochs = 100

def create_model():
  model = layers.Sequential()
  model.add(layers.Dense(42, activation='relu', input_shape=(numberOfInputs,)))
  model.add(layers.Dense(42, activation='relu'))
  model.add(layers.Dense(numberOfOutputs, activation='softmax'))
  model.compile(loss='categorical_crossentropy', optimizer="rmsprop", metrics=['accuracy'])
  return model

# results(boardHistory, gameResult) fyrir hvernig og einn leik
def train_model(results):
  global model
  input = []
  output = []
  for data in results:
    input.append(data[1])
    output.append(data[0])
  X = np.array(input).reshape((-1, numberOfInputs))
  y = keras_utils.to_categorical(output, num_classes=3)
  limit = int(0.8 * len(X))
  X_train = X[:limit]
  X_test = X[limit:]
  y_train = y[:limit]
  y_test = y[limit:]
  model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=epochs, batch_size=batchSize)

def train():
  def training_games(agents, num_games):
    # global model_evaluator
    # model.save('model.h5')
    # model_evaluator = load_model('model.h5',compile=False)
    start_time = timer()
    all_games_history, all_games_result = play.play_a_match(game, agents, num_games, 0)
    print("Time:", timer() - start_time)
    print('Match result')
    return all_games_history, all_games_result

  global model
  model = create_model()
  for round in range(1, 3):
    results = training_games(agents, 5)
    train_model(results)
  return

game = connect4.Connect4()
agent1_param = {'name':'mc_1', 'advanced': True, 'simulations':250, 'explore': 8, 'model': priors_evaluator}
agent2_param = {'name':'mc_2', 'advanced': True, 'simulations':250, 'explore': 8}
agents = [mcts_agent.MCTSAgent(agent1_param), mcts_agent.MCTSAgent(agent2_param)]
agents_eval = agents

model = None
train()