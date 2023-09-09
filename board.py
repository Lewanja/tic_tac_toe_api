import logging

logger = logging.getLogger(name=__name__)


class TicTacToeBoard:
    NUM_ROWS = NUM_COLUMNS = 3
    OPPONENT = "x"
    SERVER = "o"
    EMPTY = " "

    def __init__(self, matrix=None):
        self.board_matrix = matrix

    def from_string(self, board_string):
        board_string = board_string.lower()
        if len(board_string) != 9:
            raise ValueError("The board is not valid")
        expected_chars = {'x', 'o', ' '}
        for value in board_string:
            if value not in expected_chars:
                raise ValueError(f"{value} is invalid")
        list_board_string = list(board_string)
        first_board_row = list_board_string[0:3]
        second_board_row = list_board_string[3:6]
        third_board_row = list_board_string[6:]
        board_matrix_rep = [first_board_row, second_board_row, third_board_row]
        self.board_matrix = board_matrix_rep

    def to_string(self):
        board_matrix_single_list = ["".join(value) for value in self.board_matrix]
        board_string = "".join(board_matrix_single_list)
        return board_string

    def get_matrix_row(self, row):
        row_values = []
        for column in range(self.NUM_COLUMNS):
            board_matrix_row_values = self.board_matrix[row][column]
            row_values.append(board_matrix_row_values)
        return row_values

    def get_matrix_column(self, column):
        column_values = []
        for index in range(self.NUM_ROWS):
            board_matrix_column_values = self.board_matrix[index][column]
            column_values.append(board_matrix_column_values)
        return column_values

    def diagonal_one(self):
        diagonal = []
        for right_diagonal_row in range(self.NUM_ROWS):
            right_diagonal = self.board_matrix[right_diagonal_row][right_diagonal_row]
            diagonal.append(right_diagonal)
        return diagonal

    def diagonal_two(self):
        row_indexes = [0, 1, 2]
        column_indexes = [2, 1, 0]
        diagonals = []
        for item in range(len(row_indexes)):
            row = row_indexes[item]
            column = column_indexes[item]
            left_diagonal = self.board_matrix[row][column]
            diagonals.append(left_diagonal)

        return diagonals

    def check_can_block_opponent(self, opponent_values):
        if opponent_values.count(self.OPPONENT) == 2 and opponent_values.count(self.EMPTY) == 1:
            # empty_space_index = opponent_values.index(self.EMPTY)
            # opponent_values.pop(empty_space_index)
            # opponent_values.insert(empty_space_index, self.DEFENDER)
            return opponent_values.index(self.EMPTY)
        else:
            return None

    def check_if_server_can_win(self, cell_values):
        if cell_values.count(self.SERVER) == 2 and cell_values.count(self.EMPTY) == 1:
            return cell_values.index(self.EMPTY)
        else:
            return None

    def find_fork_opportunity(self):
        # Check each empty space for a fork opportunity.
        for row_index in range(self.NUM_ROWS):
            for column_index in range(self.NUM_COLUMNS):
                if self.board_matrix[row_index][column_index] == self.EMPTY:
                    # Make a copy of the board with 'O' placed in the empty space.
                    board_copy = [row[:] for row in self.board_matrix]
                    board_copy[row_index][column_index] = self.SERVER

                    # Check if placing 'O' at this position creates a fork.
                    fork_created = self.check_fork_created(board_copy, self.SERVER)

                    if fork_created:
                        self.board_matrix[row_index][column_index] = self.SERVER
                        return row_index, column_index  # Return the (row, column) position where 'O' creates a fork.

        return None  # No fork opportunity found.

    def check_fork_created(self, board, player):
        # Define all possible winning combinations (rows, columns, and diagonals).
        winning_combinations = [
            [(0, 0), (0, 1), (0, 2)],  # Top row
            [(1, 0), (1, 1), (1, 2)],  # Middle row
            [(2, 0), (2, 1), (2, 2)],  # Bottom row
            [(0, 0), (1, 0), (2, 0)],  # Left column
            [(0, 1), (1, 1), (2, 1)],  # Middle column
            [(0, 2), (1, 2), (2, 2)],  # Right column
            [(0, 0), (1, 1), (2, 2)],  # Diagonal from top-left to bottom-right
            [(0, 2), (1, 1), (2, 0)]  # Diagonal from top-right to bottom-left
        ]

        for combo in winning_combinations:
            line = [board[x][y] for (x, y) in combo]
            # Check if the line has two 'O's and one empty space.
            if line.count(player) == 2 and line.count(self.EMPTY) == 1:
                return True

        return False

    def find_opponent_fork(self):
        # Check for a single fork opportunity for the opponent
        possible_forks = []
        for i in range(self.NUM_ROWS):
            for j in range(self.NUM_COLUMNS):
                if self.board_matrix[i][j] == self.EMPTY:
                    # Make a copy of the board with 'X' placed in the empty space.
                    board_copy = [row[:] for row in self.board_matrix]
                    board_copy[i][j] = self.OPPONENT
                    if self.check_fork_created(board_copy, self.OPPONENT):
                        possible_forks.append((i, j))

        if len(possible_forks) == 1:
            return possible_forks[0]
        elif len(possible_forks) > 1:
            # Block all forks that do not lead to an immediate opponent fork.
            for i, j in possible_forks:
                # Make a copy of the board with 'O' placed in the empty space.
                board_copy = [row[:] for row in self.board_matrix]
                board_copy[i][j] = self.SERVER

                # Check if the opponent can create a fork in response.
                if not self.check_fork_created(board_copy, self.OPPONENT):
                    self.board_matrix[i][j] = self.SERVER
                    return i, j

        # If no forks to block, create a two in a row (if safe)
        for i in range(self.NUM_ROWS):
            for j in range(self.NUM_COLUMNS):
                if self.board_matrix[i][j] == self.EMPTY:
                    # Make a copy of the board with 'O' placed in the empty space.
                    board_copy = [row[:] for row in self.board_matrix]
                    board_copy[i][j] = self.SERVER

                    # Check if 'O' can create a two in a row without allowing a fork.
                    if self.check_two_in_a_row(board_copy):
                        self.board_matrix[i][j] = self.SERVER
                        return i, j

        return None  # No specific move found.

    def check_two_in_a_row(self, board):
        for i in range(self.NUM_ROWS):
            for j in range(self.NUM_COLUMNS):
                if board[i][j] == self.SERVER:
                    # Check if placing 'O' at this position creates a two in a row.
                    if self.check_two_in_a_row_for_player(board, i, j, self.SERVER):
                        return True
        return False

    def check_two_in_a_row_for_player(self, board, row, col, player):
        # Check for two in a row in the row, column, and diagonals that include (row, col).
        return (
                self.check_two_in_a_row_in_row(board, row, player) or
                self.check_two_in_a_row_in_column(board, col, player) or
                self.check_two_in_a_row_in_diagonals(board, row, col, player)
        )

    def check_two_in_a_row_in_row(self, board, row, player):
        # Check for two in a row in a specific row.
        row_values = board[row]
        return row_values.count(player) == 2 and row_values.count(self.EMPTY) == 1

    def check_two_in_a_row_in_column(self, board, col, player):
        # Check for two in a row in a specific column.
        col_values = [board[i][col] for i in range(self.NUM_ROWS)]
        return col_values.count(player) == 2 and col_values.count(self.EMPTY) == 1

    def check_two_in_a_row_in_diagonals(self, board, row, col, player):
        # Check for two in a row in diagonals that include (row, col).
        if row == col:
            diagonal_values = [board[i][i] for i in range(self.NUM_ROWS)]  # Main diagonal
            return diagonal_values.count(player) == 2 and diagonal_values.count(self.EMPTY) == 1
        elif row + col == self.NUM_ROWS - 1:
            diagonal_values = [board[i][self.NUM_ROWS - 1 - i] for i in range(self.NUM_ROWS)]  # Anti-diagonal
            return diagonal_values.count(player) == 2 and diagonal_values.count(self.EMPTY) == 1
        else:
            return False

    def make_move(self):
        rows = [0, 1, 2]
        for row in rows:
            row_cells = self.get_matrix_row(row)
            can_win_index = self.check_if_server_can_win(row_cells)
            if can_win_index is not None:
                self.board_matrix[row][can_win_index] = self.SERVER
                logger.info(f"possible win at {row}{can_win_index}")
                return self.to_string()
            can_block_index = self.check_can_block_opponent(row_cells)
            if can_block_index is not None:
                self.board_matrix[row][can_block_index] = self.SERVER

        columns = [0, 1, 2]
        for column in columns:
            column_cells = self.get_matrix_column(column)
            can_win_column_index = self.check_if_server_can_win(column_cells)
            if can_win_column_index is not None:
                self.board_matrix[can_win_column_index][column] = self.SERVER
                logger.info(f"possible win at {column}{can_win_column_index}")
                return self.to_string()
            can_block_column_index = self.check_can_block_opponent(column_cells)
            if can_block_column_index is not None:
                self.board_matrix[can_block_column_index][column] = self.SERVER
                return self.to_string()

        diagonal_one_value = {0: [0, 0], 1: [1, 1], 2: [2, 2]}
        cells_diagonal_one = self.diagonal_one()
        can_win_diagonals_right_index = self.check_if_server_can_win(cells_diagonal_one)
        if can_win_diagonals_right_index is not None:
            board_indexes = diagonal_one_value.get(can_win_diagonals_right_index)
            diagonal_one_row = board_indexes[0]
            diagonal_one_column = board_indexes[1]
            self.board_matrix[diagonal_one_row][diagonal_one_column] = self.SERVER
            logger.info(f"possible win at diagonal{diagonal_one_row}{diagonal_one_column}")
            return self.to_string()

        can_block_diagonals_right_index = self.check_can_block_opponent(cells_diagonal_one)
        if can_block_diagonals_right_index is not None:
            board_indexes_block = diagonal_one_value.get(can_block_diagonals_right_index)
            diagonal_one_row_block = board_indexes_block[0]
            diagonal_one_column_block = board_indexes_block[1]
            self.board_matrix[diagonal_one_row_block][diagonal_one_column_block] = self.SERVER
            return self.to_string()

        diagonal_two_value = {0: [0, 2], 1: [1, 1], 2: [2, 0]}
        cells_diagonal_two = self.diagonal_two()
        can_win_diagonals_left_index = self.check_if_server_can_win(cells_diagonal_two)
        if can_win_diagonals_left_index is not None:
            board_index_left = diagonal_two_value.get(can_win_diagonals_left_index)
            diagonal_two_row = board_index_left[0]
            diagonal_two_column = board_index_left[1]
            self.board_matrix[diagonal_two_row][diagonal_two_column] = self.SERVER
            logger.info(f"possible win at diagonal{diagonal_two_row}{diagonal_two_column}")
            return self.to_string()
        can_block_diagonals_left_index = self.check_can_block_opponent(cells_diagonal_two)
        if can_block_diagonals_left_index is not None:
            block_board_index_left = diagonal_two_value.get(can_block_diagonals_left_index)
            block_diagonal_two_row = block_board_index_left[0]
            block_diagonal_two_column = block_board_index_left[1]
            self.board_matrix[block_diagonal_two_row][block_diagonal_two_column] = self.SERVER
            logger.info(f"possible block at diagonal{block_diagonal_two_row}{block_diagonal_two_column}")
            return self.to_string()

        # To implement fork and block opponent fork
        try_fork_opportunity = self.find_fork_opportunity()
        if try_fork_opportunity is not None:
            logger.info(f"possible fork at {try_fork_opportunity}")
            return self.to_string()

        # Blocking an opponent's fork
        opponent_fork = self.find_opponent_fork()
        if opponent_fork is not None:
            self.board_matrix[opponent_fork[0]][opponent_fork[1]] = self.SERVER
            logger.info(f"possible block at {opponent_fork[0]}{opponent_fork[1]}")
            return self.to_string()
        #      check empty center and fill
        center = self.board_matrix[1][1]
        if center == self.EMPTY:
            self.board_matrix[1][1] = self.SERVER
            logger.info(f"place at center {self.board_matrix[1][1]}")
            return self.to_string()

        # check opponent opposite corners
        result = self.check_opponent_opposite_corner()
        if result is not None:
            logger.info(f"possible opponent at corner {result}")
            return result

        empty_corner_result = self.check_empty_opposite_corner()
        if empty_corner_result is not None:
            logger.info(f"possible vacant corner at corner {empty_corner_result}")
            return empty_corner_result

        empty_side_result = self.check_empty_side_corner()
        if empty_side_result is not None:
            logger.info(f"possible vacant side opponent at corner {empty_side_result }")
            return empty_side_result

    def check_opponent_opposite_corner(self):
        if self.board_matrix[0][0] == self.OPPONENT and self.board_matrix[2][2] == self.EMPTY:
            self.board_matrix[2][2] = self.SERVER
            return self.to_string()
        if self.board_matrix[2][2] == self.OPPONENT and self.board_matrix[0][0] == self.EMPTY:
            self.board_matrix[0][0] = self.SERVER
            return self.to_string()
        if self.board_matrix[2][0] == self.OPPONENT and self.board_matrix[0][2] == self.EMPTY:
            self.board_matrix[0][2] = self.SERVER
            return self.to_string()
        if self.board_matrix[0][2] == self.OPPONENT and self.board_matrix[2][0] == self.EMPTY:
            self.board_matrix[2][0] = self.SERVER
            return self.to_string()
        return None

    def check_empty_opposite_corner(self):
        if self.board_matrix[0][0] == self.EMPTY:
            self.board_matrix[0][0] = self.SERVER
            return self.to_string()
        elif self.board_matrix[2][2] == self.EMPTY:
            self.board_matrix[2][2] = self.SERVER
            return self.to_string()
        elif self.board_matrix[2][0] == self.EMPTY:
            self.board_matrix[2][0] = self.SERVER
            return self.to_string()
        elif self.board_matrix[0][2] == self.EMPTY:
            self.board_matrix[0][2] = self.SERVER
            return self.to_string()

        return None

    def check_empty_side_corner(self):
        if self.board_matrix[0][1] == self.EMPTY:
            self.board_matrix[0][1] = self.SERVER
            return self.to_string()
        elif self.board_matrix[1][0] == self.EMPTY:
            self.board_matrix[1][0] = self.SERVER
            return self.to_string()
        elif self.board_matrix[1][2] == self.EMPTY:
            self.board_matrix[1][2] = self.SERVER
            return self.to_string()
        elif self.board_matrix[2][1] == self.EMPTY:
            self.board_matrix[2][1] = self.SERVER
            return self.to_string()

        return None

    def check_win(self, player):

        row_indexes = column_indexes = [0, 1, 2]

        for row in row_indexes:
            win_row = self.get_matrix_row(row)
            win_row = [element == player for element in win_row]
            if all(win_row):
                return True

        for column in column_indexes:
            win_column = self.get_matrix_column(column)
            win_col = [value == player for value in win_column]
            if all(win_col):
                return True

        diagonal_one_value = self.diagonal_one()
        win = [item == player for item in diagonal_one_value]
        if all(win):
            return True

        diagonal_two_value = self.diagonal_one()
        win = [item == player for item in diagonal_two_value]
        if all(win):
            return True

        return False
