#!/usr/bin/env python
import psycopg2
import yaml

from generator import generator
from benchmark import benchmark

def run():
    # Initialize db
    db_connection = init_db()

    # Let the generator fill the database
    generator.run(db_connection)

    # Let the benchmark test the database
    benchmark.runBenchmark(db_connection)

    # Close the db connection.
    db_connection.close()

    return 0


def init_db():
    with open("config.yml", 'r') as config:
        cfg = yaml.load(config)

    return psycopg2.connect(host=cfg['hostname'], user=cfg['username'], password=cfg['password'], dbname=cfg['database'])
