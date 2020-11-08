import alphabeta


class AlphaBetaAgent:
    def __init__(self, params):
        self._params = params
        self.name = params.name
        return

    def name(self):
        """ Return agent's name."""
        return self.name

    def reset(self):
        """ This function clears your internal data-structures, so the next
        call to play() starts with a fresh state (ie., no history information).
        """
        # No history information is kept.
        return

    def play(self, game, check_abort):
        """ Returns the "best" move to play in the current <game>-state and its value, after some
            deliberation (<check_abort>).
        """
        return alphabeta.id_alphabeta(game, check_abort, self._params)