import sqlite3
import pandas as pd

class Database:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tuition (
                year INTEGER,
                program TEXT,
                price REAL
            )
        """)

    def save_dataframe(self, df):
        df.to_sql("tuition", self.conn, if_exists="append", index=False)

    def load_all(self):
        return pd.read_sql("SELECT * FROM tuition", self.conn)
