from tic_tac_toe.src.database import Database


class StatisticsManager:
    def __init__(self):
        self.db = Database()

    def start_game(self, player_x_id, player_o_id):
        return self.db.execute(
            """INSERT INTO games
               (player_x_id, player_o_id, winner_id, result, started_at)
               VALUES (%s, %s, NULL, 'IN_PROGRESS', NOW())""",
            (player_x_id, player_o_id)
        )

    def save_game(self, game_id, winner_id, result, moves):
        conn = self.db.connect()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """UPDATE games
                   SET winner_id = %s, result = %s, ended_at = NOW()
                   WHERE game_id = %s""",
                (winner_id, result, game_id)
            )

            if moves:
                cursor.executemany(
                    """INSERT INTO game_moves
                       (game_id, player_id, symbol, row_no, column_no, move_number)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    moves
                )

            cursor.execute(
                """UPDATE player_statistics ps
                   JOIN games g ON g.player_x_id = ps.user_id
                   SET ps.games_played = ps.games_played + 1
                   WHERE g.game_id = %s""",
                (game_id,)
            )

            cursor.execute(
                """UPDATE player_statistics ps
                   JOIN games g ON g.player_o_id = ps.user_id
                   SET ps.games_played = ps.games_played + 1
                   WHERE g.game_id = %s""",
                (game_id,)
            )

            if result == "DRAW":
                cursor.execute(
                    """UPDATE player_statistics ps
                       JOIN games g ON g.player_x_id = ps.user_id
                       SET ps.draws = ps.draws + 1, ps.score = ps.score + 1
                       WHERE g.game_id = %s""",
                    (game_id,)
                )
                cursor.execute(
                    """UPDATE player_statistics ps
                       JOIN games g ON g.player_o_id = ps.user_id
                       SET ps.draws = ps.draws + 1, ps.score = ps.score + 1
                       WHERE g.game_id = %s""",
                    (game_id,)
                )
            else:
                loser_column = "player_o_id" if result == "X" else "player_x_id"

                cursor.execute(
                    """UPDATE player_statistics ps
                       SET ps.wins = ps.wins + 1, ps.score = ps.score + 3
                       WHERE ps.user_id = %s""",
                    (winner_id,)
                )

                cursor.execute(
                    f"""UPDATE player_statistics ps
                        JOIN games g ON g.{loser_column} = ps.user_id
                        SET ps.losses = ps.losses + 1
                        WHERE g.game_id = %s""",
                    (game_id,)
                )

            conn.commit()

        except Exception:
            conn.rollback()
            raise

        finally:
            cursor.close()

    def get_user_statistics(self, user_id):
        return self.db.fetch_one(
            """SELECT u.username, ps.games_played, ps.wins,
                      ps.losses, ps.draws, ps.score
               FROM users u
               JOIN player_statistics ps ON ps.user_id = u.user_id
               WHERE u.user_id = %s""",
            (user_id,)
        )

    def get_game_history(self, user_id):
        return self.db.fetch_all(
            """SELECT g.game_id,
                      ux.username AS player_x,
                      uo.username AS player_o,
                      CASE
                        WHEN g.result = 'DRAW' THEN 'DRAW'
                        WHEN g.winner_id = %s THEN 'WIN'
                        ELSE 'LOSS'
                      END AS result,
                      g.started_at,
                      g.ended_at
               FROM games g
               JOIN users ux ON ux.user_id = g.player_x_id
               JOIN users uo ON uo.user_id = g.player_o_id
               WHERE g.player_x_id = %s OR g.player_o_id = %s
               ORDER BY g.game_id DESC""",
            (user_id, user_id, user_id)
        )

    def get_leaderboard(self):
        return self.db.fetch_all(
            """SELECT u.username, ps.games_played, ps.wins,
                      ps.losses, ps.draws, ps.score
               FROM users u
               JOIN player_statistics ps ON ps.user_id = u.user_id
               ORDER BY ps.score DESC, ps.wins DESC, u.username"""
        )
