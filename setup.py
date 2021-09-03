# This file will run once using the command line

from psycopg2 import Error
from database.connection import create_db_connection

import utils


def create_tables():
    conn = create_db_connection()

    # Getting Query from sql file to create the tables
    sql = utils.read_file("database/sql/restaurants.sql")

    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        return True
    except Error as err:
        print("Error at create_tables function. ", str(err))
    finally:
        if conn:
            cur.close()
            conn.close()


if __name__ == '__main__':
    create_tables()