# imports needed to make program run
import csv
import os
from random import seed
from random import random

from helpers.sql_helper import execute_query as query

seed(3)

# Simple routine to run a query on a database and print the results:
def doQuery(conn):
    print("Requested data:")
    print(query(conn, "SELECT * FROM m"))


# creates table in database
def create_table(conn):
    query(conn, "CREATE TABLE m ( ID VARCHAR(255), Source VARCHAR(255), TMC VARCHAR(255), Severity VARCHAR(255), Start_time VARCHAR(255), End_Time VARCHAR(255),"
                " Start_Lat VARCHAR(255), Start_Lng VARCHAR(255), End_Lat VARCHAR(255), End_lng VARCHAR(255), Distance VARCHAR(255), Description VARCHAR(255),"
                "Number VARCHAR(255), Street VARCHAR(255), Side VARCHAR(255), City VARCHAR(255), County VARCHAR(255), State VARCHAR(255), Zipcode VARCHAR(255), Country VARCHAR(255),"
                "Timezone VARCHAR(255), Airport_code VARCHAR(255), Weather_Timestamp VARCHAR(255), Temperature VARCHAR(255), Wind_Chill VARCHAR(255), Humidity VARCHAR(255),"
                "Presure VARCHAR(255), Visibility VARCHAR(255), Wind_direction VARCHAR(255), Wind_Speed VARCHAR(255), Precipitation VARCHAR(255), Weather_Condition VARCHAR(255),"
                "Amenity VARCHAR(255), Bump VARCHAR(255), Crossing VARCHAR(255), Give_Way VARCHAR(255), Junction VARCHAR(255), No_Exit VARCHAR(255), Railway VARCHAR(255), Roundabout VARCHAR(255),"
                "Station VARCHAR(255), Stop VARCHAR(255), Traffic_Calming VARCHAR(255), Traffic_Signal VARCHAR(255), Turning_loop VARCHAR(255), Sunrise_Sunset VARCHAR(255),"
                "Civil_Twilight VARCHAR(255), Nautical_Twilight VARCHAR(255), Astronomical_Twilight VARCHAR(255), Weight INT, P FLOAT);")


# Fills database
def fill_table(conn, file):
    sql = "INSERT INTO m VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    with open(file) as csv_file:
        cur = conn.cursor()
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            val = (row[0], row[1], row[2], row[3], row[4], row[5])
            if line_count == 0:
                line_count += 1
            else:
                cur.execute(sql, val)
                line_count += 1
        print("table filled completely!")


def fill_table_rows(conn, row):
    sql = "INSERT INTO m VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cur = conn.cursor()
    cur.execute(sql, row)


# fills the output file with processed data
def write_to_output(file, holder):
    with open(file, 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        writer.writerows(holder)


# shows contents of file
def show_file(file):
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print("\n" f'Column names are >> {", ".join(row)}')
                line_count += 1
            else:
                print(f'{row[0]} , {row[1]} , {row[2]} , {row[3]}, {row[4]}, {row[5]}.')
                line_count += 1
        print(f'Processed {line_count} lines.')


# alters the input file
def alter_dataset(input, output, connection):
    with open(input, 'r') as csvinput:
        holder = []
        reader = csv.reader(csvinput)
        row = next(reader)
        row.append('Weight')
        row.append('P')
        print(row)
        holder.append(row)
        index = 0

        for row in reader:
            index += 1
            inverse, value, second_value = probability_generator()
            row_value = row.copy()
            row_inverse = row.copy()

            row_value.append('1')
            row_value.append(value)
            print(row_value[49])
            fill_table_rows(connection, row_value)

            row_inverse.append('2')
            row_inverse.append(inverse)
            print(row_inverse[49])
            fill_table_rows(connection, row_inverse)

            holder.append(row_value)
            holder.append(row_inverse)

            if second_value is not 0:
                row_second_value = row.copy()
                row_second_value.append('3')
                row_second_value.append(second_value)
                print(row_second_value[49])
                fill_table_rows(connection, row_second_value)

                holder.append(row_second_value)

        print(index)
        write_to_output(output, holder)


def check_processed(input, output, connection):
    with open(output, 'r') as csvin:
        read = csv.reader(csvin)
        if os.stat(output).st_size == 0:
            alter_dataset(input, output, connection)
        else:
            check = next(read)
            if 'P' in check:
                print('File already processed!')
            else:
                alter_dataset(input, output, connection)


def probability_generator():
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
def run(connection):
    check_processed('..\\..\\data\\dataset', '..\\..\\data\\processed', connection)
    # show_file('processed')
    # create_table(connection)
    # fill_table(connection, '../data/processed')


#create_table(myConnection)
check_processed('..\\..\\data\\dataset', '..\\..\\data\\processed', myConnection)
doQuery(myConnection)


