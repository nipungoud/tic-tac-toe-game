import random

class TicTacToe:
    def __init__(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.player_score = 0
        self.ai_score = 0
        self.winner = None
        self.current_player = 'X'

    def reset_game(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.winner = None
        self.current_player = 'X'

    def make_move(self, row, col):
        if self.board[row][col] == '' and self.winner is None:
            self.board[row][col] = self.current_player
            if self.check_winner():
                self.winner = self.current_player
                if self.current_player == 'X':
                    self.player_score += 1
                else:
                    self.ai_score += 1
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def ai_move(self):
        best_score = -float('inf')
        best_move = None
        for row, col in self.get_empty_cells():
            self.board[row][col] = 'O'
            score = self.minimax(self.board, 0, False, -float('inf'), float('inf'))
            self.board[row][col] = ''
            if score > best_score:
                best_score = score
                best_move = (row, col)
        self.board[best_move[0]][best_move[1]] = 'O'
        if self.check_winner():
            self.winner = 'O'
            self.ai_score += 1
        self.current_player = 'X'

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        winner = self.check_winner()
        if winner == 'X':
            return -1
        elif winner == 'O':
            return 1
        elif self.is_board_full():
            return 0
        if is_maximizing:
            max_eval = -float('inf')
            for row, col in self.get_empty_cells():
                board[row][col] = 'O'
                eval = self.minimax(board, depth + 1, False, alpha, beta)
                board[row][col] = ''
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for row, col in self.get_empty_cells():
                board[row][col] = 'X'
                eval = self.minimax(board, depth + 1, True, alpha, beta)
                board[row][col] = ''
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def check_winner(self):
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] != '':
                return row[0]
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != '':
                return self.board[0][col]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != '':
            return self.board[0][2]
        return None

    def is_board_full(self):
        for row in self.board:
            if '' in row:
                return False
        return True

    def get_empty_cells(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == '']
    