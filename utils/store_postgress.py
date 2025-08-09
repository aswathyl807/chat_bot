import psycopg2
from psycopg2.extras import execute_values
import os
from datetime import datetime



class PostgresStore:

    def __init__(self):

        self.POSTGRES_CONFIG = {
            "dbname": os.getenv("PG_DB", "db_post"),
            "user": os.getenv("PG_USER", "postgres"),
            "password": os.getenv("PG_PASSWORD", "6100"),
            "host": os.getenv("PG_HOST", "localhost"),
            "port": os.getenv("PG_PORT", "5433"),
        }
        self.conn = psycopg2.connect(**self.POSTGRES_CONFIG)
        self.cursor = self.conn.cursor()

    def store_to_postgres(self, filename, total_pages, token_count, char_length, chunk_count):
        created_at = datetime.utcnow()
        records = [(filename, total_pages, token_count, char_length, chunk_count, created_at)]
        print(f'Inserting records: {records}')

        execute_values(self.cursor, '''
            INSERT INTO document_metadata (filename, total_pages, token_count, char_length, chunk_count, created_at)
            VALUES %s
            ON CONFLICT (filename) DO UPDATE SET
            total_pages = EXCLUDED.total_pages,
            token_count = EXCLUDED.token_count,
            char_length = EXCLUDED.char_length,
            chunk_count = EXCLUDED.chunk_count,
            created_at = EXCLUDED.created_at
        ''', records)

        self.conn.commit()


    def get_data(self):
       self.cursor.execute("SELECT * FROM document_metadata")
       rows = self.cursor.fetchall()
       return rows

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

a=PostgresStore()
a.close_connection()
