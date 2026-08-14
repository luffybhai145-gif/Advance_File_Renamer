import sqlite3
import threading


class Database:

    def __init__(self, path="bot.db"):

        self.path = path

        self.lock = threading.Lock()

        self.conn = sqlite3.connect(
            path,
            check_same_thread=False,
        )

        self.conn.row_factory = sqlite3.Row

        self.create_tables()


    def create_tables(self):

        with self.lock:

            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    user_id INTEGER NOT NULL,

                    original_name TEXT,

                    output_name TEXT,

                    created_at
                    TIMESTAMP DEFAULT CURRENT_TIMESTAMP

                )
                """
            )

            self.conn.commit()


    def add_job(
        self,
        user_id,
        original_name,
        output_name,
    ):

        with self.lock:

            cursor = self.conn.execute(
                """
                INSERT INTO jobs
                (
                    user_id,
                    original_name,
                    output_name
                )
                VALUES (?, ?, ?)
                """,
                (
                    user_id,
                    original_name,
                    output_name,
                ),
            )

            self.conn.commit()

            return cursor.lastrowid


    def get_job(self, job_id):

        cursor = self.conn.execute(
            """
            SELECT *
            FROM jobs
            WHERE id = ?
            """,
            (job_id,),
        )

        return cursor.fetchone()


    def close(self):

        self.conn.close()
