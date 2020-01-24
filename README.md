# Benchmarking MayBMS based on hardware specifications and query complexity

## Abstract
This research proposes a new kind of database that can store uncertain information: a probabilistic database. To this day, no standardized benchmark is available to assess the performance of a probabilistic database. This paper examines a benchmark for the probabilistic database ‘MayBMS’. The benchmark assesses the execution time of probabilistic queries based on the database size. An experiment is run on two hardware platforms to assess the validity of the benchmark. The benchmark creates probabilistic data and runs the benchmark queries. From the results is concluded that the number of matches for a query and the type of hardware the benchmark is executed with are of equal importance. Even though the instance with the worse hardware took considerably longer to execute, the ratio between the execution time of the queries stayed the same as on the better hardware. Thus, proving the validity of the benchmark.

[Read the paper](Paper_MayBMS_Benchmark.pdf)

## Project structure
    .
    ├── bin			# Holds all executable files
    ├── data                    # Data files (such as initial db dummy data)
    ├── maybms_benchmark        # Project files
    │   ├── benchmark           # Benchmark files
    │   │   └── ...             # All files that are needed for the benchmark
    │   ├── generator           # Data generator files
    │   │   └── ...             # All files that are needed for the data generator
    │   └── __main__.py         # Main executable project file
    │   └── app.py              # Core project script	
## Setup

This project uses PyCharm as the IDE and [Anaconda](https://www.anaconda.com/) for easy package management.

Import this project into PyCharm and execute the following in the PyCharm terminal:

```
$ bash bin/setup.sh
```

Add the file ```config.yml``` to the root of the project and fill it with your credentials:
```
hostname: ''
port: 5432
username: ''
password: ''
database: ''
```

## Dataset

Running this benchmark requires a dataset which we got from Kaggle. Place this dataset in the `/data` folder.
 
[US Traffic Accidents dataset](https://www.kaggle.com/sobhanmoosavi/us-accidents/data)

## Useful links

- [Postgres 8.3 SQL Commands](https://www.postgresql.org/docs/8.3/sql-commands.html)
- [MayBMS Language Reference](http://maybms.sourceforge.net/manual/index.html#x1-450006.2)

