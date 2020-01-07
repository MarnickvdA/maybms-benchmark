#!/usr/bin/env python
import psycopg2
import yaml
import logging

from generator import generator
from benchmark import benchmark
from helpers import sql_helper

logger = logging.getLogger()


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

    logger.info("Connecting to {}".format(cfg['hostname']))
    connection = psycopg2.connect(host=cfg['hostname'],
                                  port=cfg['port'],
                                  user=cfg['username'],
                                  password=cfg['password'],
                                  dbname=cfg['database'])
    logger.info("Connected!")

    return connection
