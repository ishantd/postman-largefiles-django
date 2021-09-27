# **Large file processor**

[LIVE DEMO](https://postman.ishantdahiya.com/)

Aim was to build a system which is able to handle **long running processes** in a **distributed fashion.** I think I have managed to do so using the following tech stack. The program is in a Monolith Architecture.

 - Django (Python Framework) - Used to create REST APIs to upload/ingest files into the DB.
 - PostgreSQL (Database)
 - Pandas and PySpark - Used to read csv files and sql commands to insert them and perform operations on the data.
 - Redis (Cache Backend) - Used to display list of products and aggregate count on the dashboard screen.

For more details on the use of PySpark please refer to: [pyspark/README.md](pyspark/README.md)

## Steps to Run the Code

This is dockerized project, and can be run by using [Docker](https://www.docker.com/) and Docker Compose

 1. Verify that your docker service is running and configured <br/>

`docker-compose run hello-world`

2. Build the Django REST API Framework to monitor and look at data stats (NOTE: This command should be used only once, when retrying to build the docker image/container please use `docker-compose up --build`)<br/>

`docker-compose up`

3. Move to the pyspark directory `cd pyspark` to build the Docker Image to ingest and aggregate data in products.csv file <br/>

`docker build -t {image_name} .`

4. Execute queries on the built docker image to ingest and perform operations on data.

`docker run {image_name} spark-submit --driver-class-path /opt/application/postgresql-42.2.24.jar main.py -p`

5. View the results after the query is successful on [Localhost](http://127.0.0.1:8000/)

### Known Issues in Docker Build Process

I found an issue while building the docker files in a **Windows** Environment. It was due the **.sh** files[namely: entrypoint.sh and entrypoint-2.sh] being in CRLF Format which is not supported in Docker **Linux** Environments. A quick fix around this would be:
1. Open the file in [Notepad++](https://notepad-plus-plus.org/downloads/)
2. go to View -> Show Symbol ->uncheck Show All Characters

## Schema Details

Since I'm using Django there are multiple tables that facilitate many inbuilt functionalities of Django as a web framework, although the only Tables that are being used in this project are:

1. Products `data_product`
	```
	CREATE TABLE data_product
	(
	    name character varying(420),
	    sku character varying(120) NOT NULL,
	    description text,
	    CONSTRAINT data_product_pkey PRIMARY KEY (sku)
	)

	```
This table has the details of all products imported from the **products.csv** file.
2. ProductAggregate `data_productaggregate`
```
			CREATE TABLE data_productaggregate
			(
				id uuid NOT NULL,
			    name character varying(420),
			    count integer,
			    CONSTRAINT data_productaggregate_pkey PRIMARY KEY (id)
			)
```
This table has the aggregate of number of products per name (customer).

## Point to Achive [Done]

 - [x] Your code should follow concept of **OOPS**
		 Implementation of OOPS Based Problem Solving in this can be found in the following files for this particular project
#### [pyspark/main.py](pyspark/main.py)
This script uses the PySpark API built on top of Apache's Spark Framework to ingest and process the data.

#### [data/utils.py](data/utils.py)
This file has a `ProcessCSV` class that handles all aspects of processing the CSV file using the REST API triggers for **dedicated PySpark Docker Cluster**.


#### [data/views.py](data/views.py)
This file has a multiple classes extending the Base `APIView` Class from Django's inbuilt functions. These are used to create **REST API Endpoints** to handle various **CRUD** operations and also to trigger file processes.

 - [x] Support for regular non-blocking parallel ingestion of the given file into a table. Consider thinking about the scale of what should happen if the file is to be processed in 2 mins.

Although with a microservice-like style architecture this program utilises Apache's greate **Spark Framework** to run ingest data parallely and in cluster modules thus allowing the user to upload and then process the files **Independent of other processes**

The [LIVE DEMO](https://postman.ishantdahiya.com/) of this project is hosted on **AWS Free Tier** hardware i.e. **1GB RAM, 1vCPU EC2 Machine and 1GB RAM, 1vCPU RDS PostgreSQL Database**

Following is the screenshot of some test runs: [Note: The upload time is actually the time taken to save the file into S3 and not the time taken for the user to upload on the internet to EC2 Machine] These can be taken with a grain of salt but are mostly accurate. I'm using the Python **timeit** library to record times and save them in a separate table.

![Image](postman_stats.png?raw=true)

 - [x] Support for updating existing products in the table based on `sku` as the primary key. (Yes, we know about the kind of data in the file. You need to find a workaround for it)
 I appended an eight length random character string at the end of the SKU to make it unique and to also let the user add more products.
 
 - [x] All product details are to be ingested into a single table
 - [x] An aggregated table on above rows with `name` and `no. of products` as the columns
	
## Point to Achive [Not Done]

I think I have completed all the points given but they can be definetely improved and optimised upon.
## Future Improvements

 - Create a **Microservices** architecture utilising Flask or other lightweight frameworks to **improve performance** and for **easy and fast scalibility**
 - Experiment with **Cache and DB Hardware Configuration** to ensure **maximum performance** of specialised tasks such as aggregation and other types of anlalytical operations.
 - Write **Unit Tests**  to ensure **reliability**
 - Research and Use specialised languages  and frameworks for these specific tasks.


## Architecture Diagram

![Image](architechture.png?raw=true)