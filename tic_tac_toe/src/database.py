import mysql.connector
from mysql.connector import Error
from tic_tac_toe.config.database_config import DB_CONFIG


class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        if self.connection and self.connection.is_connected():
            return self.connection

        self.connection = mysql.connector.connect(**DB_CONFIG)
        return self.connection

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def fetch_one(self, query, params=()):
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            return cursor.fetchone()
        finally:
            cursor.close()

    def fetch_all(self, query, params=()):
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            cursor.close()

    def execute(self, query, params=()):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()

    def execute_many(self, query, rows):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.executemany(query, rows)
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
