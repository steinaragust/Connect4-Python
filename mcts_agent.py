import mcts
import tree
import utils
import random
import tensorflow.keras as keras

class MCTSAgent:
    def __init__(self, params):
        self._params = params
        self.tree = None
        self._name = self._params.get('name')
        if self._name is None:
            self._name = "mc_agent"
        self.model = keras.models.load_model("model.h5",compile=False)
        return

    def name(self):
        """ Return agent's name."""
        return self._name

    def reset(self):
        """ This function clears your internal data-structures, so the next
        call to play() starts with a fresh state (ie., no history information).
        """
        self.tree = None
        return

    def play(self, game, check_abort):
        """ Returns the "best" move to play in the current <game>-state, after some deliberation (<check_abort>).
        """

        def display(depth, label, parent_label, i):
            for _ in range(depth):
                print('  ', end='')
            if parent_label is not None:
                print(parent_label.moves[i], parent_label.q[i].n, parent_label.q[i].avg, end=': ')
            print(label.n)
            return

        def visits(q, i):
            return q[i].n

        self.reset()
        if self.tree is None:
            self.tree = tree.Tree()

        in_advanced_mode = self._params.get('advanced')
        max_num_simulations = self._params.get('simulations')
        if max_num_simulations is None:
            max_num_simulations = 0

        num_simulations = 0
        #while not check_abort.do_abort() and (max_num_simulations == 0 or num_simulations <= max_num_simulations):
        while (max_num_simulations == 0 or num_simulations <= max_num_simulations):
            mcts.simulate(self, game, self.tree, in_advanced_mode)
            # tree.depth_first_traversal(self.tree, self.tree.root(), 0, display)
            num_simulations += 1

        node_id = self.tree.root()
        node_label = self.tree.node_label(node_id)
        max_i = utils.argmax(node_label.q, len(node_label.q), visits)
        e = self._params.get('explore')
        if e is not None and e > game.get_move_no() and random.randint(1, 10) <= 8:
            # Choose a random move with a 80% change for first e moves, if requested.
            max_i = random.randint(0, node_label.len - 1)

        policy = [node_label.q[i].n for i in range(node_label.len)]
        total = 0
        for p in policy:
            total += p
        if total > 0:
            policy = [p/total for p in policy]
        # tree.depth_first_traversal(self.tree, self.tree.root(), 0, display)
        return node_label.moves[max_i], node_label.q[max_i].avg, max_i, node_label.moves, policy, node_label.q
