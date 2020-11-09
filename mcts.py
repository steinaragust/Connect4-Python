import math
import random
import copy
import utils


class NodeLabel:
    def __init__(self, moves):
        self.moves = moves
        self.len = len(self.moves)
        self.n = 0
        self.q = [utils.Avg() for _ in range(self.len)]
        self.p = [1.0 for _ in range(self.len)]
        return


def simulate(game, tree, advanced_mode, model):
    def select(node_id):
        def puct(label, i):
            if label.q[i].n == 0:
                return utils.Infinity
            return label.q[i].avg + 0.2 * label.p[i] * (math.sqrt(label.n) / (1+label.q[i].n))

        def uct(label, i):
            if label.q[i].n == 0:
                return utils.Infinity
            return label.q[i].avg + 0.2 * (math.sqrt(math.log(label.n) / label.q[i].n))

        func = puct if advanced_mode and model else uct
        node_label = tree.node_label(node_id)
        max_i = utils.argmax(node_label, len(node_label.moves), uct, utils.Infinity)
        return max_i, node_label.moves[max_i]

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
            if advanced_mode:
                move = moves[utils.argmax(moves, len(moves), learn.prior_no, utils.Infinity)]
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

    def evaluate(node_id):
        # In AZ, would call NN here to get priors and value.
        label = tree.node_label(node_id)
        for i, m in enumerate(label.moves):
            label.p[i] = learn.prior(m)
        return learn.state_value(game)


    def traverse(depth, node_id, parent_id):
        if node_id is None:
            if advanced_mode and model is not None:
                new_node_id = expand(parent_id)
                value = evaluate(new_node_id)
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
