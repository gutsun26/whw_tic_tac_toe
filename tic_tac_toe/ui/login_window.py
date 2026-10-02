import tkinter as tk
from tkinter import messagebox

from tic_tac_toe.src.user import UserManager
from tic_tac_toe.ui.register_window import RegisterWindow
from tic_tac_toe.ui.game_window import GameWindow


class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe - Login")
        self.root.geometry("420x420")
        self.root.resizable(False, False)

        self.user_manager = UserManager()
        self.users = []

        self.build_ui()
        self.refresh_users()

    def build_ui(self):
        tk.Label(
            self.root, text="TIC-TAC-TOE",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Player X", font=("Arial", 12, "bold")).grid(
            row=0, column=0, padx=10, pady=8
        )

        self.x_var = tk.StringVar()
        self.x_menu = tk.OptionMenu(frame, self.x_var, "")
        self.x_menu.config(width=18)
        self.x_menu.grid(row=0, column=1)

        tk.Label(frame, text="Player O", font=("Arial", 12, "bold")).grid(
            row=1, column=0, padx=10, pady=8
        )

        self.o_var = tk.StringVar()
        self.o_menu = tk.OptionMenu(frame, self.o_var, "")
        self.o_menu.config(width=18)
        self.o_menu.grid(row=1, column=1)

        tk.Button(
            self.root, text="Start Game",
            font=("Arial", 14, "bold"),
            width=18, command=self.start_game
        ).pack(pady=20)

        tk.Button(
            self.root, text="Register New User",
            font=("Arial", 12),
            width=18, command=self.open_register
        ).pack(pady=5)

        tk.Button(
            self.root, text="Exit",
            font=("Arial", 12),
            width=18, command=self.root.destroy
        ).pack(pady=5)

    def refresh_users(self):
        try:
            self.users = self.user_manager.get_all_users()
        except Exception as exc:
            messagebox.showerror("Database Error", str(exc))
            return

        menu_x = self.x_menu["menu"]
        menu_o = self.o_menu["menu"]

        menu_x.delete(0, "end")
        menu_o.delete(0, "end")

        for user in self.users:
            menu_x.add_command(
                label=user["username"],
                command=lambda value=user["username"]: self.x_var.set(value)
            )
            menu_o.add_command(
                label=user["username"],
                command=lambda value=user["username"]: self.o_var.set(value)
            )

        if self.users:
            self.x_var.set(self.users[0]["username"])
            self.o_var.set(
                self.users[1]["username"] if len(self.users) > 1
                else self.users[0]["username"]
            )

    def open_register(self):
        RegisterWindow(self.root, self.refresh_users)

    def start_game(self):
        x_name = self.x_var.get()
        o_name = self.o_var.get()

        if not x_name or not o_name:
            messagebox.showwarning("Login", "Select both players.")
            return

        if x_name == o_name:
            messagebox.showwarning(
                "Login", "Player X and Player O must be different users."
            )
            return

        x_user = next(u for u in self.users if u["username"] == x_name)
        o_user = next(u for u in self.users if u["username"] == o_name)

        self.root.withdraw()
        GameWindow(
            self.root,
            x_user,
            o_user,
            self.show_login
        )

    def show_login(self):
        self.root.deiconify()

    def run(self):
        self.root.mainloop()
