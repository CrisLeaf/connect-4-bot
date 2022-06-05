import numpy as np
import time


ROWS_COUNT = 6
COLUMNS_COUNT = 7

class GameBot():
    def __init__(self, rows_count=ROWS_COUNT, columns_count=COLUMNS_COUNT):
        self.rows_count = rows_count
        self.columns_count = columns_count

    def _get_column_available_position(self, board, column):
        try:
            available_position = np.where(board[:, column] != 0)[0][0] - 1
        except:
            available_position = self.rows_count - 1

        return available_position

    def _get_available_position(self, board, column):
        available_columns = []

        for col in range(self.columns_count):
            available_position = self._get_column_available_position(board, col)

            if available_position >= 0:
                available_columns.append(col)

        return available_columns

    def _get_next_possible_moves(self, board, piece, first_iteration=False):
        possibles_list = []

        for j in range(self.columns_count):
            board_copy = board.copy()

            available_position = self._get_column_available_position(board, column=j)

            if available_position >= 0:
                board_copy[available_position, j] = piece
                possibles_list.append(board_copy)
            elif first_iteration:
                possibles_list.append("Invalid move")

        return possibles_list

    def _get_available_columns(self, board):
        available_columns = []

        for col in range(self.columns_count):
            available_position = self._get_column_available_position(board, col)

            if available_position >= 0:
                available_columns.append(col)

        return available_columns

    def _translate_board(self, b):
        output_board = np.array([
            [int(b[0]),  int(b[1]),  int(b[2]),  int(b[3]),  int(b[4]),  int(b[5]),  int(b[6])],
            [int(b[7]),  int(b[8]),  int(b[9]),  int(b[10]), int(b[11]), int(b[12]), int(b[13])],
            [int(b[14]), int(b[15]), int(b[16]), int(b[17]), int(b[18]), int(b[19]), int(b[20])],
            [int(b[21]), int(b[22]), int(b[23]), int(b[24]), int(b[25]), int(b[26]), int(b[27])],
            [int(b[28]), int(b[29]), int(b[30]), int(b[31]), int(b[32]), int(b[33]), int(b[34])],
            [int(b[35]), int(b[36]), int(b[37]), int(b[38]), int(b[39]), int(b[40]), int(b[41])],
        ])

        return np.where(output_board >= 2, -1, output_board)

    def _is_winning_move(self, board, piece):
        for c in range(self.columns_count - 3):
            for r in range(self.rows_count):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                    return True

    	#Check vertical
        for c in range(self.columns_count):
            for r in range(self.rows_count - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                    return True

    	# Check positive slope diagonal
        for c in range(self.columns_count - 3):
            for r in range(self.rows_count - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                    return True

    	# Check negative slope diagonal
        for c in range(self.columns_count - 3):
            for r in range(3, self.rows_count):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                    return True

        return False


    def _get_simulated_score(self, board, next_turn):
        sim_board = board.copy()

        for i in range(42):
            piece = next_turn * (-1)**i
            available_columns = self._get_available_columns(sim_board)

            if len(available_columns) == 0:
                return 0

            random_col = np.random.choice(available_columns)

            available_position = self._get_column_available_position(sim_board, random_col)

            if available_position >= 0:
                sim_board[available_position, random_col] = piece

            if self._is_winning_move(sim_board, piece):
                return piece * (-1)

        return 0


    def get_next_move(self, board):
        board = self._translate_board(board)

        number_of_pieces = 0

        for row in board:
            for c in row:
                if c != 0:
                    number_of_pieces += 1

        if number_of_pieces == 1:
            if self._get_column_available_position(board, 3) == 5:
                time.sleep(0.8)
                return 3
            else:
                time.sleep(0.8)
                return np.random.choice([2, 4])

        # number_of_sims = int(np.log2(number_of_pieces) + 3)
        # number_of_sims = int(number_of_pieces**(2) / 100) + 2
        number_of_sims = int(number_of_pieces**(4) / 200_000) + 2

        # Get next moves
        next_move_list = self._get_next_possible_moves(board, -1, first_iteration=True)

        # Second moves
        second_moves_list = []

        for move in next_move_list:
            if type(move) == str:
                second_moves_list.append("Invalid move")
            else:
                next_moves = self._get_next_possible_moves(move, 1)
                second_moves_list.append(next_moves)

        # Third moves
        third_moves_list = []

        for moves_list in second_moves_list:
            if type(moves_list) == str:
                third_moves_list.append("Invalid move")

                continue

            sub_list = []

            for index, move in enumerate(moves_list):
                next_moves = self._get_next_possible_moves(move, -1)

                for next_move in next_moves:
                    sub_list.append(next_move)

            third_moves_list.append(sub_list)

        # Simulate
        scores_list = []

        for moves_list in third_moves_list:
            if type(moves_list) == str:
                scores_list.append(-1000)

                continue

            sub_list = []
            random_iter = np.random.choice([i for i in range(10, 21)])

            for move in moves_list:
                for _ in range(number_of_sims):
                    score = self._get_simulated_score(move, next_turn=1)
                    sub_list.append(score)

            scores_list.append(np.sum(sub_list))

        return scores_list.index(max(scores_list))


if __name__ == "__main__":
    bot = GameBot()

    next = int(bot.get_next_move("000000000000000000000000000000000000000100"))
    print("type:", type(next))
    print("suggested next:", next)
