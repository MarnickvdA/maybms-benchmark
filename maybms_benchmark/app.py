#!/usr/bin/env python
import yaml
import psycopg2
import psycopg2.extensions
import logging
import pandas as pd
from datetime import datetime
import os

from maybms_benchmark.generator import generator
from maybms_benchmark.benchmark import benchmark
from maybms_benchmark.helpers import sql_helper
from maybms_benchmark.helpers.fs_helper import get_project_root as project_root

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def run():
    """
    This function runs the totality of the benchmark. It injects the right data in the configured MayBMS database and
    executes queries to capture the performance of the MayBMS system. Finally, it will generate a file with the results
    of the benchmark.
    """
    # Initialize db
    connection = init_db()
    sql_helper.nuke_tables(connection)

    logger.info("Populating probabilistic database...")
    number_of_elements = 10000
    generator.run(connection, size=number_of_elements)
    logger.info("Populating complete!")

    # Let the benchmark test the database
    benchmark_results = benchmark.runBenchmark(connection, logger)

    # Clear the database
    logger.info("Clearing the database...")
    sql_helper.nuke_tables(connection)
    logger.info("Clear complete")

    # Close the db connection.
    connection.close()
    logger.info("Database connection ended.")

    # Save the results to a file
    date_time = datetime.now().strftime("%Y%m%d-%H%M")
    export_results(results=benchmark_results, filename="{}_{}-elements_maybms-benchmark-result.csv".format(date_time, number_of_elements))

    logger.info("Bye!")


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


def export_results(results, filename):
    df = pd.DataFrame.from_dict(results, orient='index', columns=['execution_time'])
    filename = os.path.join(project_root(), "results", filename)
    df.to_csv(filename)
    logger.info("Results exported to {}".format(filename))
