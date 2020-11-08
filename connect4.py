import numpy as np

class Connect4:
    PLAYER_1 = 0
    PLAYER_2 = 1

    OPPONENT = [PLAYER_2, PLAYER_1]

    EMPTY = 0
    PLAYER_1_PIECE = 1
    PLAYER_2_PIECE = 2

    def __init__(self, params):
        self.ROW_COUNT = 6
        self.COLUMN_COUNT = 7

        self.WINDOW_LENGTH = 4
        self.setup()
        return

    def get_board(self):
        return self.board

    def setup(self):
        self.board = self.create_board()
        self.turn = self.PLAYER_1

    def get_piece(self):
        if self.turn == self.PLAYER_1:
            return self.PLAYER_1_PIECE
        return self.PLAYER_2_PIECE

    def get_opponent_piece(self):
        if self.turn == self.PLAYER_1:
            return self.PLAYER_2_PIECE
        return self.PLAYER_1_PIECE

    def create_board(self):
        board = np.zeros((self.ROW_COUNT, self.COLUMN_COUNT))
        return board

    def drop_piece_top_column(self, col):
        row = self.get_next_open_row(col)
        piece = self.get_to_move()
        self.drop_piece(self, col, row, piece)


    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece
        self.turn = self.OPPONENT[self.turn]

    def retract_piece(self, row, col):
        self.board[row][col] = self.EMPTY
        self.turn = self.OPPONENT[self.turn]

    def is_valid_location(self, col):
        return self.board[self.ROW_COUNT - 1][col] == 0

    def get_next_open_row(self, col):
        for r in range(self.ROW_COUNT):
            if self.board[r][col] == 0:
                return r

    def print_board(self):
        print(np.flip(self.board, 0))

    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT):
                if (
                    self.board[r][c] == piece
                    and self.board[r][c + 1] == piece
                    and self.board[r][c + 2] == piece
                    and self.board[r][c + 3] == piece
                ):
                    return True

        # Check vertical locations for win
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT - 3):
                if (
                    self.board[r][c] == piece
                    and self.board[r + 1][c] == piece
                    and self.board[r + 2][c] == piece
                    and self.board[r + 3][c] == piece
                ):
                    return True

        # Check positively sloped diaganols
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT - 3):
                if (
                    self.board[r][c] == piece
                    and self.board[r + 1][c + 1] == piece
                    and self.board[r + 2][c + 2] == piece
                    and self.board[r + 3][c + 3] == piece
                ):
                    return True

        # Check negatively sloped diaganols
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(3, self.ROW_COUNT):
                if (
                    self.board[r][c] == piece
                    and self.board[r - 1][c + 1] == piece
                    and self.board[r - 2][c + 2] == piece
                    and self.board[r - 3][c + 3] == piece
                ):
                    return True


    def is_terminal_node(self):
        return (
            self.winning_move(self.PLAYER_1_PIECE)
            or self.winning_move(self.PLAYER_2_PIECE)
            or len(self.get_valid_locations()) == 0
        )

    def get_valid_locations(self):
        valid_locations = []
        for col in range(self.COLUMN_COUNT):
            if self.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations

    def get_to_move(self):
        return self.turn
