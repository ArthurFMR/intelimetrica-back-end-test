import os
import psycopg2


DATABASE_URL = os.environ.get("DATABASE_URL", None)
LOCAL_DB_CONFIG = {"dbname": "restaurant", "user": "postgres", "password": "Admin2021"}


def create_connection():
    try:
        conn = None
        if DATABASE_URL:
            # Cloud DB connection
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            return conn
        # Local DB Connection
        conn = psycopg2.connect(**LOCAL_DB_CONFIG)
        return conn
    except psycopg2.Error as Err:
        print("Error at create_connection func. | ", str(Err))
