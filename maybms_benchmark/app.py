#!/usr/bin/env python
import psycopg2
import yaml
import time
import psycopg2
import psycopg2.extensions
from psycopg2.extras import LoggingConnection, LoggingCursor
import logging

from generator import generator
from benchmark import benchmark
from helpers import sql_helper


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# MyLoggingCursor simply sets self.timestamp at start of each query
class MyLoggingCursor(LoggingCursor):
    def execute(self, query, vars=None):
        self.timestamp = time.time()
        return super(MyLoggingCursor, self).execute(query, vars)

    def callproc(self, procname, vars=None):
        self.timestamp = time.time()
        return super(MyLoggingCursor, self).callproc(procname, vars)


# MyLogging Connection:
#   a) calls MyLoggingCursor rather than the default
#   b) adds resulting execution (+ transport) time via filter()
class MyLoggingConnection(LoggingConnection):
    def filter(self, msg, curs):
        return msg + "   %d ms" % int((time.time() - curs.timestamp) * 1000)

    def cursor(self, *args, **kwargs):
        kwargs.setdefault('cursor_factory', MyLoggingCursor)
        return LoggingConnection.cursor(self, *args, **kwargs)


def run():
    """
    This function runs the totality of the benchmark. It injects the right data in the configured MayBMS database and
    executes queries to capture the performance of the MayBMS system. Finally, it will generate a file with the results
    of the benchmark.
    """
    # Initialize logging
    init_logging()

    # Initialize db
    connection = init_db()

    # Let the generator fill the database
    # generator.run(db_connection)

    # Let the benchmark test the database
    # results = benchmark.runBenchmark(db_connection)

    # Clear the database
    # sql_helper.nuke_tables(connection)

    # Close the db connection.
    connection.close()
    logger.info("Connection closed")

    # Save the results to a file
    # TODO


def init_logging():
    """
    Configures the logger for debugging
    """
    logging.basicConfig(level=logging.DEBUG, format='[ %(asctime)-15s ] %(message)s')
    logger.info('Initialization of the logger is complete')


def init_db():
    """
    Initializes the database connection with psycopg2 and the local config.yml file
    :return: database connection
    """
    with open("../config.yml", 'r') as config:
        cfg = yaml.load(config, Loader=yaml.FullLoader)

    logger.info("Connecting to {} on port {}".format(cfg['hostname'], cfg['port']))
    connection = psycopg2.connect(host=cfg['hostname'],
                                  port=cfg['port'],
                                  user=cfg['username'],
                                  password=cfg['password'],
                                  dbname=cfg['database'])
    logger.info("Connected!")

    return connection
