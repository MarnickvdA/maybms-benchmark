# maybms-benchmark

## Introduction
Predicting if a patient has a certain disease could be of great value. This prediction would be based on historical data of patients with likewise symptoms for a disease. If this data is entered into a database, many rows and columns will be produced. Rows can either be completely filled, partially filled or empty. These partially filled rows contain so-called missing values. It is possible to just disregard these missing values, but this could lead to a bias in the dataset. It would be better to predict what these values should have been. Through comparing the symptoms of different patients, it is possible to calculate the probability of our patient having disease A or disease B. This creates a so-called probabilistic database. These probabilistic databases could be of great value to minimize the amount of missing values. 

This research project will provide a benchmark for comparing these databases. The benchmark will include a scalable data generator capable of producing probabilistic datasets. This research will solely focus on MayBMS. Other probabilistic databases are out of the scope of this project.

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
    └── setup.py		# Initializes this project's package
	
## Setup

This project uses PyCharm as the IDE and [Anaconda](https://www.anaconda.com/) for easy package management.

Import this project into PyCharm and execute the following in the PyCharm terminal:

```
$ bash bin/setup.sh
```

## Usage

...
