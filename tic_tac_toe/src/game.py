class TicTacToeGame:
    def __init__(self, player_x_id, player_o_id):
        self.player_x_id = player_x_id
        self.player_o_id = player_o_id
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_over = False

    def make_move(self, row, col):
        if self.game_over or self.board[row][col] != "":
            return None

        self.board[row][col] = self.current_player

        winner = self.check_winner()
        if winner:
            self.game_over = True
            return winner

        if self.check_draw():
            self.game_over = True
            return "DRAW"

        self.current_player = "O" if self.current_player == "X" else "X"
        return None

    def check_winner(self):
        for row in range(3):
            if self.board[row][0] != "" and \
               self.board[row][0] == self.board[row][1] == self.board[row][2]:
                return self.board[row][0]

        for col in range(3):
            if self.board[0][col] != "" and \
               self.board[0][col] == self.board[1][col] == self.board[2][col]:
                return self.board[0][col]

        if self.board[0][0] != "" and \
           self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return self.board[0][0]

        if self.board[0][2] != "" and \
           self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return self.board[0][2]

        return None

    def check_draw(self):
        return all(cell != "" for row in self.board for cell in row)

    def get_player_id(self, symbol):
        return self.player_x_id if symbol == "X" else self.player_o_id
