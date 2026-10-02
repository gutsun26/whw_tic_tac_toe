import tkinter as tk
from tkinter import messagebox

from tic_tac_toe.src.user import UserManager


class RegisterWindow:
    def __init__(self, parent, callback):
        self.window = tk.Toplevel(parent)
        self.window.title("Register User")
        self.window.geometry("350x280")
        self.window.resizable(False, False)

        self.callback = callback
        self.manager = UserManager()

        tk.Label(
            self.window, text="Create User",
            font=("Arial", 20, "bold")
        ).pack(pady=15)

        frame = tk.Frame(self.window)
        frame.pack()

        tk.Label(frame, text="Username").grid(row=0, column=0, padx=8, pady=8)
        self.username_entry = tk.Entry(frame, width=22)
        self.username_entry.grid(row=0, column=1)

        tk.Label(frame, text="Password").grid(row=1, column=0, padx=8, pady=8)
        self.password_entry = tk.Entry(frame, width=22, show="*")
        self.password_entry.grid(row=1, column=1)

        tk.Label(frame, text="Confirm").grid(row=2, column=0, padx=8, pady=8)
        self.confirm_entry = tk.Entry(frame, width=22, show="*")
        self.confirm_entry.grid(row=2, column=1)

        tk.Button(
            self.window, text="Register",
            width=15, command=self.register
        ).pack(pady=15)

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()

        if password != confirm:
            messagebox.showwarning("Register", "Passwords do not match.")
            return

        try:
            success, message = self.manager.register(username, password)
        except Exception as exc:
            messagebox.showerror("Database Error", str(exc))
            return

        if success:
            messagebox.showinfo("Register", message)
            self.callback()
            self.window.destroy()
        else:
            messagebox.showwarning("Register", message)
