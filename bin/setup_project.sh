#!/usr/bin/env bash

# Commands that require you to be logged into your conda environment
# This project was made for and with PyCharm. Be sure to check out how to configure conda
# in the IDE: https://www.jetbrains.com/help/pycharm-edu/conda-support-creating-conda-virtual-environment.html

echo Installing additional libraries...
conda install -c anaconda psycopg2
conda install -c anaconda yaml
conda install -c anaconda pandas
4