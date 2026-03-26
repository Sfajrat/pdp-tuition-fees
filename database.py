import sqlite3
import pandas as pd

class Database:
    def __init__(self, path="tuition.db"):
        self.conn = sqlite3.connect(path)

        # Создаём таблицу
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tuition (
                year INTEGER,
                program TEXT,
                program_length INTEGER,
                students_count INTEGER,
                price REAL,
                university TEXT
            )
        """)
        self.conn.commit()

    def save_dataframe(self, df):
        df.to_sql("tuition", self.conn, if_exists="append", index=False)

    def load_all(self):
        return pd.read_sql("SELECT * FROM tuition", self.conn)
