from psycopg2 import Error
import csv

from database.connection import create_db_connection
import utils


def calculate_geom_column(restaurant_id, conn: object):
    sql = f"""UPDATE restaurants SET geom = ST_SetSRID(ST_MakePoint(lng, lat), 4326)
             WHERE id = '{restaurant_id}' """

    try:
        cur = conn.cursor()
        cur.execute(sql)
    except Error as err:
        print("Error at calculate_geom_column function. ", err)


def load_csv_data(url: str):
    conn = create_db_connection() # Creating DB Connection
    file_path = utils.download_file('restaurants.csv', url)
    file = open(file_path, encoding="ISO-8859-1")
    sql = "INSERT INTO restaurants VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    try:
        cur = conn.cursor()
        rows = csv.reader(file)
        next(rows) # Skip header row

        for row in rows:
            row[1] = int(row[1]) # Casting 'rating' column to int
            cur.execute(sql, row)
            calculate_geom_column(row[0], conn) # row[0] is the id cell

        conn.commit()
        return True
    except Error as err:
        print("Error at load_csv_data function. ", str(err))
        return False
    finally:
        file.close()
        if conn:
            cur.close()
            conn.close()


def insert(data):
    conn = create_db_connection()

    sql = """INSERT INTO restaurants 
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    try:
        cur = conn.cursor()
        cur.execute(sql, data)
        calculate_geom_column(data[0], conn) # data[0] is the id record
        conn.commit()
        return True
    except Error as err:
        print("Error at insert restaurant function. ", err)
        return False