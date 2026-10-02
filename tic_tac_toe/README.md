# Tic-Tac-Toe — Tkinter + MySQL

## Features

- Two registered users play against each other.
- Player X and Player O are selected from the database.
- User registration.
- Passwords stored as SHA-256 hashes rather than plain text.
- Game result stored in MySQL.
- Every move stored in MySQL.
- Wins, losses, draws and score stored per user.
- Game history.
- Statistics window.
- C-style modular folder organization.
- Class-based Python implementation.

## Score

- Win = 3 points
- Draw = 1 point
- Loss = 0 points

## 1. Install MySQL

Create a MySQL database by executing:

    sql/database.sql

For example, using MySQL command line:

    mysql -u root -p < sql/database.sql

## 2. Configure the application

Open:

    config/database_config.py

Change:

    YOUR_MYSQL_PASSWORD

to your MySQL root password.

## 3. Install Python dependency

    pip install -r requirements.txt

## 4. Run

From the tic_tac_toe directory:

    python main.py

## Important

Run `main.py` from the project root so Python can find the config,
src and ui packages.
