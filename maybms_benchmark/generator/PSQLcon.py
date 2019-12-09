# imports needed to make program run
import psycopg2
import csv
import os
from random import seed
from random import random

# Keys to connect to Maybms database
hostname = 'localhost'
username = ''
password = ''
database = 'template1'
processedFlag = 1
holder = []
seed(3)

# Simple routine to run a query on a database and print the results:
def doQuery( conn ) :
    print("Requested data:")
    cur = conn.cursor()
    cur.execute("SELECT * FROM k")

    for value in cur.fetchall():
        print(value)

def open_output():
    with open('processed.txt', 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        writer.writerows(holder)

def show_file():
    with open('processed.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print("\n" f'Column names are >> {", ".join(row)}')
                line_count += 1
            else:
                print(f'\t{row[0]} , {row[1]} , {row[2]} , {row[3]}.')
                line_count += 1
        print(f'Processed {line_count} lines.')

def cvs_reader():
    with open('datasets.txt', 'r') as csvinput:
        reader = csv.reader(csvinput)
        row = next(reader)
        row.append(' P')
        print(row)
        holder.append(row)

        for row in reader:
            inverse, value = probability_generator()
            row_value = row.copy()
            row_inverse = row.copy()
            row_value.append(value)
            row_inverse.append(inverse)
            holder.append(row_value)
            holder.append(row_inverse)

        open_output()
        #show_file

def check_processed():
    with open('processed.txt','r') as csvin:
        read = csv.reader(csvin)
        if os.stat('processed.txt').st_size == 0:
            cvs_reader()
        else:
            check = next(read)
            if 'P' in check:
                print('File already processed!')
            else:
                cvs_reader()

def probability_generator():
    value = random()
    inverse = 1-value
    return inverse, value


# prints the requested values to command prompt
myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database )
doQuery(myConnection)
myConnection.close()
check_processed()


