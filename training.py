import tensorflow.keras as keras
import tensorflow.keras.layers as layers
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential,Model
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout, BatchNormalization, LeakyReLU,Input,Add,Concatenate
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
batchSize = 128
epochs = 100

def output_represention(moves, policy):
  tensor = np.zeros(7)
  for i, p in enumerate(policy):
    tensor[moves[i]] = p
  return tensor

def create_model():
  Input_1= Input(shape=(42, ),name="input")

  x = Dense(42, activation='relu')(Input_1)
  x = BatchNormalization()(x)
  x = Dense(84, activation='relu')(x)
  x = BatchNormalization()(x)
  x = Dense(42, activation='relu')(x)
  x = BatchNormalization()(x)

  out1 = Dense(7, name="policy", activation='softmax')(x)

  out2 = Dense(10, activation='relu')(x)
  out2 = BatchNormalization()(out2)
  out2 = Dense(1, name="value",  activation='linear')(out2)


  model = Model(inputs=Input_1, outputs=[out1,out2])
  model.compile(
      optimizer="adam",
      loss={
        "policy": keras.losses.CategoricalCrossentropy(from_logits=True),
        "value": 'mean_squared_error',
      },
      loss_weights=[0.3, 0.7],
      metrics=['accuracy']
)
  return model


def train_model(model, X, Y, Z):
  X = np.array(X)
  Y = np.array(Y)
  Z = np.array(Z)
  #Y = to_categorical(Y, num_classes=7)
  limit = int(0.8 * len(X))
  X_train = X[:limit]
  X_test = X[limit:]
  y_train = Y[:limit]
  y_test = Y[limit:]
  Z_train = Z[:limit]
  Z_test = Z[limit:]
  model.fit(
    {"input": X_train},
    {"policy": y_train, "value": Z_train},
   # {"input": X_test},
   # {"policy": y_test, "value": Z_test}, 
    epochs=epochs
    
)

def train():
  def to_training_data(game, result, agentname):
    X = []
    Y = []
    Z = []
    draws = result[3]
    if result[0][0] == agentname:
      outcome = result[2]
      agent = 0
    elif result[0][1] == agentname:
      outcome = -result[2]
      agent = 1
    else:
      print('Oops, agent not playing!')
      return X, Y, Z
    game.setup()
    for i, return_value in enumerate(result[1]):
      move, value, max_i, moves, policy, q = return_value
      if i % 2 == agent:
        X.append(game.get_board().flatten())
        Y.append(output_represention(moves, policy))
        Z.append(value)
      game.drop_piece_in_column(move)
    return np.array(X), np.array(Y), np.array(Z)


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


  global model
  for _ in range(0, 10):
    X = []
    Y = []
    Z = []
    results = training_games(agents, 10)
    for result in results:
      x, y, z = to_training_data(game, result, agents[0].name())
      X.extend(x)
      Y.extend(y)
      Z.extend(z)
    train_model(model, X, Y, Z)
  return

game = connect4.Connect4()
model = None
model = create_model()
agent1_param = {'name':'mc_AZ', 'advanced': False, 'simulations':150, 'explore': 5, 'model': model}
agent2_param = {'name':'mc_standard', 'advanced': False, 'simulations':50, 'explore': 5}
agents = [mcts_agent.MCTSAgent(agent1_param), mcts_agent.MCTSAgent(agent2_param)]
agents_eval = agents

train()
model.save('model.h5')