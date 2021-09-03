from psycopg2 import Error
import psycopg2.extras
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
        utils.remove_file(file_path)
        
        if conn:
            cur.close()
            conn.close()


def insert(data: tuple):
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
    finally:
        if conn:
            cur.close()
            conn.close()


def select_all():
    conn = create_db_connection()

    sql = """SELECT id, rating, name, site, email, phone, street, city
                    state, lat, lng 
             FROM restaurants"""

    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql)
        results = cur.fetchall()
        return results
    except Error as err:
        print("Error at select_all restaurants function. ", str(err))
    finally:
        if conn:
            cur.close()
            conn.close()


def update(data: tuple):
    conn = create_db_connection()

    sql = """UPDATE restaurants
                SET rating = %s, name = %s, site = %s, email = %s, 
                    phone = %s, street = %s, city = %s, state = %s, 
                    lat = %s, lng = %s
                WHERE id = %s
            """
    
    try:
        cur = conn.cursor()
        cur.execute(sql, data)
        calculate_geom_column(data[0], conn) # data[0] is the id record
        conn.commit()
        return True
    except Error as err:
        print("Error at update restaurant function. ", err)
        return False


def delete(_id):
    conn = create_db_connection()

    sql = "DELETE FROM restaurants WHERE id = %s"
    
    try:
        cur = conn.cursor()
        cur.execute(sql, (_id,))
        conn.commit()
        return True
    except Error as err:
        print("Error at delete restaurant function. ", err)
        return False


def find_restaurants_in_circle(lng, lat, radius):
    conn = create_db_connection()
    param = (lng, lat, radius)

    sql = """
    SELECT COUNT(id), AVG(rating), STDDEV(rating)
        FROM restaurants
    WHERE ST_DWithin(geom, ST_MakePoint(%s, %s)::geography, %s)
    """

    try:
        cur = conn.cursor()
        cur.execute(sql, param)
        results = cur.fetchall()
        return results
    except Error as err:
        print("Error at find_restaurants_in_circle restaurants function. ", str(err))
    finally:
        if conn:
            cur.close()
            conn.close()