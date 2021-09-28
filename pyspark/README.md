# **PySpark and Apache Spark**

This module uses Python API for Spark released by the Apache Spark community to ingest the products.csv file and perform operations on it and analyze it.

## Steps to build docker image and run operations

1. `docker build -t pystest .`

#### `docker run pystest spark-submit --driver-class-path /opt/application/postgresql-42.2.24.jar main.py --options`

This command can be used to perform various operations on the CSV file and the PostgreSQL Database

Options Include:

- `docker run pystest spark-submit --driver-class-path /opt/application/postgresql-42.2.24.jar main.py -p` <br> Use  **-p** to ingest the CSV File and append the products to the PostgreSQL Table and also perform aggregate operation on it.

- `docker run pystest spark-submit --driver-class-path /opt/application/postgresql-42.2.24.jar main.py -a` <br> Use  **-a** to run the aggregate function on the products table.
