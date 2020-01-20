# imports needed to make program run
import csv
from random import seed
from random import random
import os

from helpers.sql_helper import execute_query as query

seed(3)


# Simple routine to run a query on a database and print the results:
def doQuery(conn):
    print("Requested data:")
    value = query(conn, "SELECT * FROM m", True)
    print(value)


# drops the table from the database
def drop_table(conn):
    query(conn, "DROP TABLE m")


# creates table in database
def create_table(conn):
    cur = conn.cursor()
    cur.execute("CREATE TABLE m ( ID VARCHAR(255), Source VARCHAR(255), TMC VARCHAR(255), Severity VARCHAR(255), Start_time DATE, End_Time DATE,"
                " Start_Lat VARCHAR(255), Start_Lng VARCHAR(255), End_Lat VARCHAR(255), End_lng VARCHAR(255), Distance VARCHAR(255), Description VARCHAR(255),"
                "Number VARCHAR(255), Street VARCHAR(255), Side VARCHAR(255), City VARCHAR(255), County VARCHAR(255), State VARCHAR(255), Zipcode VARCHAR(255), Country VARCHAR(255),"
                "Timezone VARCHAR(255), Airport_code VARCHAR(255), Weather_Timestamp VARCHAR(255), Temperature VARCHAR(255), Wind_Chill VARCHAR(255), Humidity VARCHAR(255),"
                "Presure VARCHAR(255), Visibility VARCHAR(255), Wind_direction VARCHAR(255), Wind_Speed VARCHAR(255), Precipitation VARCHAR(255), Weather_Condition VARCHAR(255),"
                "Amenity VARCHAR(255), Bump VARCHAR(255), Crossing VARCHAR(255), Give_Way VARCHAR(255), Junction VARCHAR(255), No_Exit VARCHAR(255), Railway VARCHAR(255), Roundabout VARCHAR(255),"
                "Station VARCHAR(255), Stop VARCHAR(255), Traffic_Calming VARCHAR(255), Traffic_Signal VARCHAR(255), Turning_loop VARCHAR(255), Sunrise_Sunset VARCHAR(255),"
                "Civil_Twilight VARCHAR(255), Nautical_Twilight VARCHAR(255), Astronomical_Twilight VARCHAR(255), Weight INT, P FLOAT);")
    conn.commit()

# fills the table in the database
def fill_table_rows(conn, row):
    cur = conn.cursor()
    sql = "INSERT INTO m VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30], row[31], row[32],row[33], row[34], row[35], row[36], row[37], row[38], row[39], row[40], row[41], row[42], row[43], row[44], row[45], row[46], row[47], row[48], row[49], row[50])
    cur.execute(sql, val)
    conn.commit()


# alters the input file
def alter_dataset(input, connection, size):
    with open(input, 'r') as csvinput:
        reader = csv.reader(csvinput)
        row = next(reader)
        row.append('Weight')
        row.append('P')
        index = 0

        for row in reader:
            if index > size:
                return
            if len(row) == 49:
                index += 1
                inverse, value, second_value = probability_generator()
                row_value = row.copy()
                row_inverse = row.copy()

                row_value.append('1')
                row_value.append(value)
                fill_table_rows(connection, row_value)

                row_inverse.append('2')
                row_inverse.append(inverse)
                fill_table_rows(connection, row_inverse)

                if second_value is not 0:
                    row_second_value = row.copy()
                    row_second_value.append('3')
                    row_second_value.append(second_value)
                    fill_table_rows(connection, row_second_value)


def probability_generator():
    """
    Generate probabilities for the rows in the dataset.
    :return: probability values
    """
    value = random()
    second_value = 0
    if value < 0.5:
        while True:
            second_value = random()
            if second_value < 0.5:
                inverse = 1 - (value + second_value)
                break
    else:
        inverse = 1 - value
    return inverse, value, second_value


# Generates data and fills database
def run(connection, size):
    create_table(connection)
    alter_dataset('..\\data\\dataset', connection, size)






