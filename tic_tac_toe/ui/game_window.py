import tkinter as tk
from tkinter import messagebox

from tic_tac_toe.src.game import TicTacToeGame
from tic_tac_toe.src.statistics import StatisticsManager
from tic_tac_toe.ui.statistics_window import StatisticsWindow


class GameWindow:
    def __init__(self, parent, player_x, player_o, on_close):
        self.parent = parent
        self.player_x = player_x
        self.player_o = player_o
        self.on_close = on_close

        self.window = tk.Toplevel(parent)
        self.window.title("Tic-Tac-Toe")
        self.window.geometry("500x700")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        self.game = TicTacToeGame(
            player_x["user_id"],
            player_o["user_id"]
        )
        self.statistics = StatisticsManager()
        self.game_id = self.statistics.start_game(
            player_x["user_id"],
            player_o["user_id"]
        )

        self.moves = []
        self.move_number = 0

        self.build_ui()

    def build_ui(self):
        tk.Label(
            self.window, text="TIC-TAC-TOE",
            font=("Arial", 26, "bold")
        ).pack(pady=15)

        tk.Label(
            self.window,
            text=f"X : {self.player_x['username']}    |    "
                 f"O : {self.player_o['username']}",
            font=("Arial", 13)
        ).pack(pady=5)

        self.status = tk.Label(
            self.window,
            text=f"{self.player_x['username']}'s turn (X)",
            font=("Arial", 16, "bold")
        )
        self.status.pack(pady=15)

        frame = tk.Frame(self.window)
        frame.pack(pady=10)

        self.buttons = []

        for row in range(3):
            button_row = []

            for col in range(3):
                button = tk.Button(
                    frame,
                    text="",
                    font=("Arial", 32, "bold"),
                    width=4,
                    height=2,
                    command=lambda r=row, c=col: self.button_click(r, c)
                )
                button.grid(row=row, column=col, padx=4, pady=4)
                button_row.append(button)

            self.buttons.append(button_row)

        tk.Button(
            self.window,
            text="Statistics",
            font=("Arial", 12),
            width=15,
            command=self.show_statistics
        ).pack(pady=12)

        tk.Button(
            self.window,
            text="New Game",
            font=("Arial", 12),
            width=15,
            command=self.new_game
        ).pack(pady=5)

        tk.Button(
            self.window,
            text="Back to Login",
            font=("Arial", 12),
            width=15,
            command=self.close
        ).pack(pady=5)

    def button_click(self, row, col):
        symbol = self.game.current_player

        if self.game.board[row][col] != "":
            return

        result = self.game.make_move(row, col)

        self.move_number += 1
        player_id = self.game.get_player_id(symbol)

        self.moves.append((
            self.game_id,
            player_id,
            symbol,
            row,
            col,
            self.move_number
        ))

        self.buttons[row][col].config(text=symbol)

        if result == "X" or result == "O":
            winner = self.player_x if result == "X" else self.player_o

            self.statistics.save_game(
                self.game_id,
                winner["user_id"],
                result,
                self.moves
            )

            messagebox.showinfo(
                "Game Over",
                f"{winner['username']} ({result}) wins!"
            )
            self.new_game()
            return

        if result == "DRAW":
            self.statistics.save_game(
                self.game_id,
                None,
                "DRAW",
                self.moves
            )

            messagebox.showinfo("Game Over", "It's a draw!")
            self.new_game()
            return

        player = (
            self.player_x
            if self.game.current_player == "X"
            else self.player_o
        )

        self.status.config(
            text=f"{player['username']}'s turn ({self.game.current_player})"
        )

    def new_game(self):
        self.game = TicTacToeGame(
            self.player_x["user_id"],
            self.player_o["user_id"]
        )

        self.game_id = self.statistics.start_game(
            self.player_x["user_id"],
            self.player_o["user_id"]
        )

        self.moves = []
        self.move_number = 0

        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="")

        self.status.config(
            text=f"{self.player_x['username']}'s turn (X)"
        )

    def show_statistics(self):
        StatisticsWindow(
            self.window,
            self.player_x,
            self.player_o
        )

    def close(self):
        self.window.destroy()
        self.on_close()
