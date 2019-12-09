
def execute_query(connection, query):

    # Create new cursor for this db connection.
    cur = connection.cursor()

    # Added explain analyze for query performance data. https://statsbot.co/blog/postgresql-query-optimization/
    cur.execute("EXPLAIN ANALYZE {}".format(query))

    # Retrieve the result.
    result = cur.fetchall()

    # Commit the update
    connection.commit()

    # Close the current cursor
    cur.close()

    # Return the result.
    return result

