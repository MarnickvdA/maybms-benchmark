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
    print(query(conn, "SELECT * FROM k"))


def write_to_output(file, holder):
    with open(file, 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        writer.writerows(holder)


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


def alter_dataset(input, output):
    with open(input, 'r') as csvinput:
        holder = []
        reader = csv.reader(csvinput)
        row = next(reader)
        row.append('Weight')
        row.append('P')
        print(row)
        #holder.clear()
        holder.append(row)

        for row in reader:
            inverse, value, second_value = probability_generator()
            row_value = row.copy()
            row_inverse = row.copy()

            row_value.append('1')
            row_value.append(value)

            row_inverse.append('2')
            row_inverse.append(inverse)

            holder.append(row_value)
            holder.append(row_inverse)

            if second_value is not 0:
                row_second_value = row.copy()
                row_second_value.append('3')
                row_second_value.append(second_value)
                holder.append(row_second_value)

        write_to_output(output, holder)


def check_processed(input, output):
    with open(output, 'r') as csvin:
        read = csv.reader(csvin)
        if os.stat(output).st_size == 0:
            alter_dataset(input, output)
        else:
            check = next(read)
            if 'P' in check:
                print('File already processed!')
            else:
                alter_dataset(input, output)


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

def run(connection):
    print("hello")
    # Do cool generator stuff...
    # ...


check_processed('dataset', 'processed')
show_file('processed')
