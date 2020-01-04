#!/usr/bin/env python
import psycopg2
import yaml
import logging

from generator import generator
from benchmark import benchmark

logger = logging.getLogger()


def run():
    # Initialize logging
    init_logging()

    # Initialize db
    db_connection = init_db()

    # Let the generator fill the database
    # generator.run(db_connection)

    # Let the benchmark test the database
    benchmark.runBenchmark(db_connection)

    # Close the db connection.

    db_connection.close()
    logger.info("Connection closed")

    return 0


def init_logging():
    logging.basicConfig(level=logging.DEBUG, format='[ %(asctime)-15s ] %(message)s')
    logger.info('Initialization of the logger is complete')


def init_db():
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
