import psycopg2
from psycopg2.extras import execute_values
import os
from datetime import datetime
from utils.store_postgress import PostgresStore
import time

post_store = PostgresStore()



def get_data(self):
       self.cursor.execute("SELECT * FROM document_metadata")
       rows = self.cursor.fetchall()
       return rows

