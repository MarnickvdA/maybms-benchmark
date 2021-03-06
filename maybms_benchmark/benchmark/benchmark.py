import timeit

from helpers.sql_helper import execute_query as query
from helpers.sql_helper import create_probabilistic_table as create_ptable

# Running on top of Postgres 8.3: https://www.postgresql.org/docs/8.3/sql-commands.html
# Language reference for MayBMS: http://maybms.sourceforge.net/manual/index.html#x1-450006.2

# Amount of iterations of the queries
TEST_CYCLES = 3


def runBenchmark(connection, logger):
    logger.info("Starting the benchmark!")

    # Create probabilistic table with name S, use as key '' from the table X and with probability column 'P'
    create_ptable(connection, new_table_name="p_table", repair_key="ID", from_table="m", p_column_name="P")

    # Case 1: where
    query_1 = "SELECT " \
              "ID, tconf() " \
              "FROM p_table " \
              "WHERE Weight = 1 AND ID = 'A-1';"


    # Case 2: advanced where
    query_2 = "SELECT " \
              "ID, Start_Time, End_Time, tconf() " \
              "FROM p_table " \
              "WHERE End_time < date '2018-07-20 00:00:00' " \
              "AND Start_Time > date '2016-03-09 00:00:00';"

    # Case 3: where and group by
    query_3 = "SELECT " \
              "conf() " \
              "FROM p_table " \
              "WHERE Start_Time <= date '2017-04-20 00:00:00' " \
              "AND Temperature <= '40'" \
              "GROUP BY city;"

    # case 4: advanced where and group by
    query_4 = "SELECT " \
              "City, ID, Severity, tconf() as prob " \
              "FROM p_table " \
              "WHERE Start_Time >= date '2016-04-09 00:00:00' " \
              "AND End_Time <= date '2018-05-12 : 00:00:00' " \
              "AND Astronomical_Twilight = 'Night' " \
              "AND Source = 'MapQuest' " \
              "AND Severity = '2' " \
              "GROUP BY ID, City, Severity, prob;"

    # case 5: simple where self join
    query_5 = "SELECT A.ID as ID1, B.ID as ID2, A.City, tconf() " \
              "FROM P_table A, P_table B " \
              "WHERE A.ID <> B.ID " \
              "AND A.City = B.city " \
              "AND A.Start_Time <= date '2016-08-01 00:00:00' " \
              "AND A.Severity = '2' " \
              "AND B.Weather_Condition = 'Rain' " \
              "ORDER BY A.City;"

    # case 6: simple union
    query_6 = "SELECT " \
              "ID, Start_Time, Severity, tconf() " \
              "FROM p_table " \
              "WHERE Start_time < date '2016-07-20 00:00:00' " \
              "UNION " \
              "SELECT " \
              "ID, Start_Time, Weather_Condition, tconf() " \
              "FROM p_table " \
              "WHERE Start_time > date '2017-07-20 00:00:00' " \
              "ORDER BY Start_Time"


    # Execute the queries that are defined above, so the database puts them in the cache
    logger.info("Executing queries for caching functionality")

    query(connection=connection, query=query_1, fetch=True)
    query(connection=connection, query=query_2, fetch=True)
    query(connection=connection, query=query_3, fetch=True)
    query(connection=connection, query=query_4, fetch=True)
    query(connection=connection, query=query_5)
    query(connection=connection, query=query_6)

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

    delta_time_query_5 = timeit.timeit(lambda: query(connection, query_5), number=TEST_CYCLES) / TEST_CYCLES
    logger.info("Query 5: Complete.")

    delta_time_query_6 = timeit.timeit(lambda: query(connection, query_6), number=TEST_CYCLES) / TEST_CYCLES
    logger.info("Query 6: Complete.")


    # Saving the results in a summarized dictionary
    summary = dict([
        ('Query 1', [delta_time_query_1]),
        ('Query 2', [delta_time_query_2]),
        ('Query 3', [delta_time_query_3]),
        ('Query 4', [delta_time_query_4]),
        ('Query 5', [delta_time_query_5]),
        ('Query 6', [delta_time_query_6]),
    ])

    # Return the query execution results
    return summary
