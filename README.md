# maybms-benchmark

## Introduction
Predicting if a patient has a certain disease could be of great value. This prediction would be based on historical data of patients with likewise symptoms for a disease. If this data is entered into a database, many rows and columns will be produced. Rows can either be completely filled, partially filled or empty. These partially filled rows contain so-called missing values. It is possible to just disregard these missing values, but this could lead to a bias in the dataset. It would be better to predict what these values should have been. Through comparing the symptoms of different patients, it is possible to calculate the probability of our patient having disease A or disease B. This creates a so-called probabilistic database. These probabilistic databases could be of great value to minimize the amount of missing values. 

This research project will provide a benchmark for comparing these databases. The benchmark will include a scalable data generator capable of producing probabilistic datasets. This research will solely focus on MayBMS. Other probabilistic databases are out of the scope of this project.

## Technologies
Project is created with:
* Lorem version: 12.3
* Ipsum version: 2.33
* Ament library version: 999
	
## Setup
To run this project, install it locally using npm:

```
$ cd ../lorem
$ npm install
$ npm start
```
