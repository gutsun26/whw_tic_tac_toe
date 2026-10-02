CREATE DATABASE IF NOT EXISTS tic_tac_toe;

USE tic_tac_toe;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(30) NOT NULL UNIQUE,
    password_hash CHAR(64) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS player_statistics (
    user_id INT PRIMARY KEY,
    games_played INT NOT NULL DEFAULT 0,
    wins INT NOT NULL DEFAULT 0,
    losses INT NOT NULL DEFAULT 0,
    draws INT NOT NULL DEFAULT 0,
    score INT NOT NULL DEFAULT 0,
    CONSTRAINT fk_stats_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS games (
    game_id INT AUTO_INCREMENT PRIMARY KEY,
    player_x_id INT NOT NULL,
    player_o_id INT NOT NULL,
    winner_id INT NULL,
    result VARCHAR(15) NOT NULL,
    started_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ended_at DATETIME NULL,

    CONSTRAINT fk_game_x
        FOREIGN KEY (player_x_id)
        REFERENCES users(user_id),

    CONSTRAINT fk_game_o
        FOREIGN KEY (player_o_id)
        REFERENCES users(user_id),

    CONSTRAINT fk_game_winner
        FOREIGN KEY (winner_id)
        REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS game_moves (
    move_id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT NOT NULL,
    player_id INT NOT NULL,
    symbol CHAR(1) NOT NULL,
    row_no INT NOT NULL,
    column_no INT NOT NULL,
    move_number INT NOT NULL,

    CONSTRAINT fk_move_game
        FOREIGN KEY (game_id)
        REFERENCES games(game_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_move_player
        FOREIGN KEY (player_id)
        REFERENCES users(user_id)
);
