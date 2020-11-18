import math
import random
import copy
import utils
import numpy as np
import tensorflow.keras as keras

class NodeLabel:
    def __init__(self, moves):
        self.moves = moves
        self.len = len(self.moves)
        self.n = 0
        self.q = [utils.Avg() for _ in range(self.len)]
        self.p = [1.0 for _ in range(self.len)]
        return

def simulate(self, game, tree, advanced_mode):
    def predict():
        x = game.get_board().flatten()
        x = np.reshape(x, (1, -1))
<<<<<<< HEAD
        #priors = self.model.predict(x)
        priors, value = self.model(x, training=False)
        return priors[0], value[0]
=======
        priors = self.model(x, training=False)
        return priors[0].numpy()
>>>>>>> 6586779b388b8d1e479dffca0d2686b147008850

    def select(node_id):
        def puct(label, i):
            if label.q[i].n == 0:
                return utils.Infinity
            return label.q[i].avg + 0.2 * label.p[i] * (math.sqrt(label.n) / (1+label.q[i].n))

        def uct(label, i):
            if label.q[i].n == 0:
                return utils.Infinity
            return label.q[i].avg + 0.2 * (math.sqrt(math.log(label.n) / label.q[i].n))

        func = puct if advanced_mode else uct
        node_label = tree.node_label(node_id)
        max_i = utils.argmax(node_label, len(node_label.moves), func, utils.Infinity)
        #if len([0 for x in node_label.q if x.n != 0]) == 7:
            #print('hi')
        return max_i, node_label.moves[max_i]

    def bias(game, moves):
        for m in moves:
            game.drop_piece_in_column(m)
            winning_move = game.winning_move()
            game.retract_piece_in_column(m)
            if winning_move:
                return m
        return None

    def get_best_move_from_nn(predictions, moves):
        available_moves = [(p, i) for i, p in enumerate(predictions) if i in moves]
        return sorted(available_moves, key=lambda x: x[0], reverse=True)[0][1]



    def playout(g):
        # def bias(moves, i):
        #     m = moves[i]
        #     to_row = g.get_board().row(m[1])
        #     if to_row == 0 or to_row == g.get_board().rows() - 1:
        #         return utils.Infinity  # A move winning immediately.
        #     return 0 if m[2] == g.get_board().NoPce else 1  # A non-capture vs. capture move.
        player = g.get_to_move()
        while not g.is_terminal_node():
            moves = g.get_valid_locations()
            winning_move = bias(g, moves)
            if winning_move is not None:
                move = winning_move
            elif advanced_mode:
                predictions = predict()
                move = moves.index[np.where(predictions == np.argmax(predictions))]
            else:
                move = moves[random.randint(0, len(moves) - 1)]
            g.drop_piece_in_column(move)
        return -1.0 if g.get_to_move() == player else 1.0

    def expand(node_id):
        node_label = NodeLabel(game.get_valid_locations())
        if node_id is None:
            node_id = tree.add_root(node_label)
        else:
            node_id = tree.add_child(node_id, node_label)
        return node_id

    def backup_update(node_id, i, value):
        label = tree.node_label(node_id)
        label.n += 1
        label.q[i].add(value)
        return

    def get_priors(node_id):
        # In AZ, would call NN here to get priors and value.
        label = tree.node_label(node_id)
        predictions, value = predict()
        moves = game.get_valid_locations()
        for i, m in enumerate(moves):
            label.p[i] = predictions[m]
<<<<<<< HEAD
        return value
=======
>>>>>>> 6586779b388b8d1e479dffca0d2686b147008850

    def traverse(depth, node_id, parent_id):
        if node_id is None:
            if advanced_mode:
                new_node_id = expand(parent_id)
<<<<<<< HEAD
                value = evaluate(new_node_id)
=======
                get_priors(new_node_id)
                value = playout(copy.deepcopy(game))
>>>>>>> 6586779b388b8d1e479dffca0d2686b147008850
            else:
                value = playout(copy.deepcopy(game))
                expand(parent_id)
        else:
            if game.is_terminal_node():
                value = -1.0   # Loss for player to move.
            else:
                i, column = select(node_id)
                game.drop_piece_in_column(column)
                value = -traverse(depth+1, tree.child(node_id, i), node_id)
                game.retract_piece_in_column(column)
                backup_update(node_id, i, value)
        return value

    traverse(0, tree.root(), None)
    return
