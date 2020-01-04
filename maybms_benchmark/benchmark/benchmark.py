import timeit

from helpers.sql_helper import execute_query as query
from helpers.sql_helper import create_probabilistic_table as create_ptable

# Running on top of Postgres 8.3: https://www.postgresql.org/docs/8.3/sql-commands.html
# Language reference for MayBMS: http://maybms.sourceforge.net/manual/index.html#x1-450006.2

# Amount of iterations of the queries
TEST_CYCLES = 3

# Case 1: where
QUERY_1 = "SELECT " \
          "l_returnflag, l_linestatus, conf() " \
          "FROM lineitem " \
          "WHERE l_shipdate <= date '1998-09-01';"

# Case 2: advanced where
QUERY_2 = "SELECT " \
          "l_returnflag, l_linestatus, conf() " \
          "FROM lineitem " \
          "WHERE l_shipdate <= date '1998-09-01' " \
          "AND l_shipdate => date '1990-01-01';"

# Case 3: where and group by
QUERY_3 = "SELECT " \
          "l_returnflag, l_linestatus, conf() " \
          "FROM lineitem " \
          "WHERE l_shipdate <= date '1998-09-01' " \
          "GROUP BY l_returnflag, l_linestatus;"

# case 4: advanced where and group by
QUERY_4 = "SELECT " \
          "l_returnflag, l_linestatus, conf() " \
          "FROM lineitem " \
          "WHERE l_shipdate <= date '1998-09-01' " \
          "o_orderdate >= date '1993-07-01' " \
          "AND o_orderdate < date '1993-10-01' " \
          "AND l_orderkey = o_orderkey " \
          "AND l_commitdate < l_receiptdate " \
          "GROUP BY l_returnflag, l_linestatus;"

# case 5: Joins ?
QUERY_5 = ""


def runBenchmark(connection):
    # create_ptable(connection=, new_table_name=, repair_key=, from_table=, P_column_name=)

    # Execute the queries that are defined above.
    delta_time_query_1 = timeit.timeit(lambda: query(connection, QUERY_1), number=TEST_CYCLES) / TEST_CYCLES
    delta_time_query_2 = timeit.timeit(lambda: query(connection, QUERY_2), number=TEST_CYCLES) / TEST_CYCLES
    delta_time_query_3 = timeit.timeit(lambda: query(connection, QUERY_3), number=TEST_CYCLES) / TEST_CYCLES
    delta_time_query_4 = timeit.timeit(lambda: query(connection, QUERY_4), number=TEST_CYCLES) / TEST_CYCLES
    delta_time_query_5 = timeit.timeit(lambda: query(connection, QUERY_5), number=TEST_CYCLES) / TEST_CYCLES

    # Saving the results in a summarized dictionary
    summary = dict([
        (1, delta_time_query_1),
        (2, delta_time_query_2),
        (3, delta_time_query_3),
        (4, delta_time_query_4),
        (5, delta_time_query_5),
    ])

    # Return the query execution results
    return summary
