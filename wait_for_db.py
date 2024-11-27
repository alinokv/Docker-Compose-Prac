import time
import psycopg2
from psycopg2 import OperationalError

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                dbname='New',
                user='postgres',
                password='123',
                host='db',
                port='5432'
            )
            conn.close()
            break
        except OperationalError:
            print("Database not ready yet. Waiting...")
            time.sleep(5)

if __name__ == "__main__":
    wait_for_db()
