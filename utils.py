from timeit import default_timer as timer

Infinity = 10000

class CheckAbort:
    def __init__(self, avail_time):
        self._avail_time = avail_time
        self._start_time = timer()

    def do_abort(self):
        if self._avail_time == 0:
            return False
        return timer() - self._start_time >= self._avail_time

class Avg:

    def __init__(self):
        self.n = 0
        self.avg = 0.0

    def add(self, v):
        self.n += 1
        self.avg += (v - self.avg) / self.n


def argmax(data, n, evaluate, maximum_value=None):
    max_i = 0
    max_v = evaluate(data, 0)
    if max_v == maximum_value:
        return max_i
    for i in range(n):
        value = evaluate(data, i)
        if value == maximum_value:
            return i
        if value > max_v:
            max_i = i
            max_v = value
    return max_i

def evaluate_window(game, window, piece):
    score = 0
    piece_score = 0
    if window.count(piece) == 4:
        piece_score += 100
    elif window.count(piece) == 3 and window.count(game.EMPTY) == 1:
        piece_score += 5
    elif window.count(piece) == 2 and window.count(game.EMPTY) == 2:
        piece_score += 2

    return score

def score_position(game):
    board = game.get_board()
    turn = game.get_piece()
    totalScore = 0
    center_array = [int(i) for i in list(board[:, game.COLUMN_COUNT // 2])]
    for piece in game.PIECES:
        score = 0
        ## Score center column
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(game.ROW_COUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(game.COLUMN_COUNT - 3):
                window = row_array[c: c + game.WINDOW_LENGTH]
                score += evaluate_window(game, window, piece)

        ## Score Vertical
        for c in range(game.COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(game.ROW_COUNT - 3):
                window = col_array[r: r + game.WINDOW_LENGTH]
                score += evaluate_window(game, window, piece)

        ## Score posive sloped diagonal
        for r in range(game.ROW_COUNT - 3):
            for c in range(game.COLUMN_COUNT - 3):
                window = [board[r + i][c + i] for i in range(game.WINDOW_LENGTH)]
                score += evaluate_window(game, window, piece)

        for r in range(game.ROW_COUNT - 3):
            for c in range(game.COLUMN_COUNT - 3):
                window = [board[r + 3 - i][c + i] for i in range(game.WINDOW_LENGTH)]
                score += evaluate_window(game, window, piece)
        totalScore += (1 if piece == turn else -1) * score
    return totalScore

