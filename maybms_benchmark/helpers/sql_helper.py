def drop_table(connection, table_name):
    execute_query(connection, "DROP TABLE {} CASCADE".format(table_name))


def create_probabilistic_table(connection, new_table_name, repair_key, from_table, P_column_name):
    execute_query(connection, "create table {} as repair key {} in {} weight by {};".format(new_table_name, repair_key, from_table, P_column_name))


def get_probabilistic_query(table_name, from_table):
    return "create table {} as select conf() as P from {}".format(table_name, from_table)


def execute_query(connection, query, fetch=False):
    # Create new cursor for this db connection.
    cur = connection.cursor()

    cur.execute("{}".format(query))

    # Retrieve the result.
    result = 0

    if fetch:
        result = cur.fetchall()

    # Commit the update
    connection.commit()

    # Close the current cursor
    cur.close()

    # Return the result.
    return result
