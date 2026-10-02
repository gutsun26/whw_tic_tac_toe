import tkinter as tk
from tkinter import ttk, messagebox

from src.statistics import StatisticsManager


class StatisticsWindow:
    def __init__(self, parent, player_x, player_o):
        self.window = tk.Toplevel(parent)
        self.window.title("Player Statistics")
        self.window.geometry("760x560")
        self.window.resizable(False, False)

        self.manager = StatisticsManager()

        self.player_x = player_x
        self.player_o = player_o

        self.build_ui()
        self.load_data()

    def build_ui(self):
        tk.Label(
            self.window,
            text="PLAYER STATISTICS",
            font=("Arial", 22, "bold")
        ).pack(pady=15)

        stats_frame = tk.Frame(self.window)
        stats_frame.pack(pady=5)

        self.x_stats = tk.Label(
            stats_frame,
            text="",
            font=("Arial", 12),
            justify="left"
        )
        self.x_stats.grid(row=0, column=0, padx=25)

        self.o_stats = tk.Label(
            stats_frame,
            text="",
            font=("Arial", 12),
            justify="left"
        )
        self.o_stats.grid(row=0, column=1, padx=25)

        tk.Label(
            self.window,
            text="Game History",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        columns = (
            "id", "x", "o", "result",
            "started", "ended"
        )

        self.tree = ttk.Treeview(
            self.window,
            columns=columns,
            show="headings",
            height=10
        )

        headings = {
            "id": "Game",
            "x": "Player X",
            "o": "Player O",
            "result": "Result",
            "started": "Started",
            "ended": "Ended"
        }

        widths = {
            "id": 55,
            "x": 120,
            "o": 120,
            "result": 75,
            "started": 150,
            "ended": 150
        }

        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(column, width=widths[column])

        self.tree.pack(padx=10, pady=5)

        tk.Button(
            self.window,
            text="Refresh",
            width=12,
            command=self.load_data
        ).pack(pady=10)

    def load_data(self):
        try:
            x = self.manager.get_user_statistics(
                self.player_x["user_id"]
            )
            o = self.manager.get_user_statistics(
                self.player_o["user_id"]
            )

            x_history = self.manager.get_game_history(
                self.player_x["user_id"]
            )
        except Exception as exc:
            messagebox.showerror("Database Error", str(exc))
            return

        self.x_stats.config(
            text=(
                f"X: {x['username']}\n"
                f"Games: {x['games_played']}\n"
                f"Wins: {x['wins']}\n"
                f"Losses: {x['losses']}\n"
                f"Draws: {x['draws']}\n"
                f"Score: {x['score']}"
            )
        )

        self.o_stats.config(
            text=(
                f"O: {o['username']}\n"
                f"Games: {o['games_played']}\n"
                f"Wins: {o['wins']}\n"
                f"Losses: {o['losses']}\n"
                f"Draws: {o['draws']}\n"
                f"Score: {o['score']}"
            )
        )

        for item in self.tree.get_children():
            self.tree.delete(item)

        for game in x_history:
            self.tree.insert(
                "",
                "end",
                values=(
                    game["game_id"],
                    game["player_x"],
                    game["player_o"],
                    game["result"],
                    game["started_at"],
                    game["ended_at"]
                )
            )
