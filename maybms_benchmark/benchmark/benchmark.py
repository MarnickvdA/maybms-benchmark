import timeit

from helpers.sql_helper import execute_query as query
from helpers.sql_helper import create_probabilistic_table as create_ptable

# Running on top of Postgres 8.3: https://www.postgresql.org/docs/8.3/sql-commands.html
# Language reference for MayBMS: http://maybms.sourceforge.net/manual/index.html#x1-450006.2

# Amount of iterations of the queries
TEST_CYCLES = 3


def runBenchmark(connection, logger):
    # Create probabilistic table with name S, use as key '' from the table X and with probability column 'P'
    create_ptable(connection, new_table_name="p_table", repair_key="", from_table="m", p_column_name="P")

    # Case 1: where
    query_1 = "SELECT " \
              "ID, l_linestatus, conf() " \
              "FROM P_table " \
              "WHERE humidity <= 90;"

    # Case 2: advanced where
    query_2 = "SELECT " \
              "l_returnflag, l_linestatus, conf() " \
              "FROM lineitem " \
              "WHERE l_shipdate <= date '1998-09-01' " \
              "AND l_shipdate => date '1990-01-01';"

    # Case 3: where and group by
    query_3 = "SELECT " \
              "l_returnflag, l_linestatus, conf() " \
              "FROM lineitem " \
              "WHERE l_shipdate <= date '1998-09-01' " \
              "GROUP BY l_returnflag, l_linestatus;"

    # case 4: advanced where and group by
    query_4 = "SELECT " \
              "l_returnflag, l_linestatus, conf() " \
              "FROM lineitem " \
              "WHERE l_shipdate <= date '1998-09-01' " \
              "o_orderdate >= date '1993-07-01' " \
              "AND o_orderdate < date '1993-10-01' " \
              "AND l_orderkey = o_orderkey " \
              "AND l_commitdate < l_receiptdate " \
              "GROUP BY l_returnflag, l_linestatus;"

    # case 5: Joins ?
    query_5 = ""

    # Execute the queries that are defined above, so the database puts them in the cache
    logger.info("Executing queries for caching functionality")
    query(connection=connection, query=query_1)
    query(connection=connection, query=query_2)
    query(connection=connection, query=query_3)
    query(connection=connection, query=query_4)
    query(connection=connection, query=query_5)

    # Run the benchmark with cached queries
    logger.info("Running benchmark!")
    delta_time_query_1 = timeit.timeit(lambda: query(connection, query_1, fetch=True), number=TEST_CYCLES) / TEST_CYCLES
    logger.info("Query 1: Complete.")

    delta_time_query_2 = timeit.timeit(lambda: query(connection, query_2, fetch=True), number=TEST_CYCLES) / TEST_CYCLES
    logger.info("Query 2: Complete.")

    delta_time_query_3 = timeit.timeit(lambda: query(connection, query_3, fetch=True), number=TEST_CYCLES) / TEST_CYCLES
    logger.info("Query 3: Complete.")

    delta_time_query_4 = timeit.timeit(lambda: query(connection, query_4, fetch=True), number=TEST_CYCLES) / TEST_CYCLES
    logger.info("Query 4: Complete.")

    delta_time_query_5 = timeit.timeit(lambda: query(connection, query_5, fetch=True), number=TEST_CYCLES) / TEST_CYCLES
    logger.info("Query 5: Complete.")


    # Saving the results in a summarized dictionary
    summary = dict([
        ('Query 1', [delta_time_query_1]),
        ('Query 2', [delta_time_query_2]),
        ('Query 3', [delta_time_query_3]),
        ('Query 4', [delta_time_query_4]),
        ('Query 5', [delta_time_query_5]),
    ])

    # Return the query execution results
    return summary
