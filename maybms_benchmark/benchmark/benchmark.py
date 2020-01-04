from helpers.sql_helper import execute_query as query


# Running on top of Postgres 8.3: https://www.postgresql.org/docs/8.3/sql-commands.html
# Language reference for MayBMS: http://maybms.sourceforge.net/manual/index.html#x1-450006.2

def runBenchmark(connection):
    # Dummy case
    print(query(connection, "SELECT * FROM *"))

    # Take a database table R with the column P, to create a probabilistic database we must use the statement 'repair key'.
    # This creates a tuple of the possible outcomes paired with the probability that the event occurs

    # create table S as
    # repair key Dummy in R weight by P;

    # Now that we have a probabilistic table S, we can use the statement 'conf()' to do queries according to the confidence

    # Case 1: where

    # Case 2: where, group by

    # Case 3: weight by

    # Case 4:

    # Case 5: sorting by probability

    return 0
