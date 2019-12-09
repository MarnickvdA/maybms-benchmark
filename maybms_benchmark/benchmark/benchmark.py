from helpers.sql_helper import execute_query as query


def runBenchmark(connection):
    # Case 1
    query(connection, "SELECT * FROM *")

    return 0
