FROM datamechanics/spark:3.1-latest

ENV PYSPARK_MAJOR_PYTHON_VERSION=3

USER root

WORKDIR /opt/application/

COPY requirements.txt .
RUN apt-get update
RUN apt-get install libpq-dev gcc -y
COPY products.csv .
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir Cython
RUN pip3 install wheel && pip3 install -r requirements.txt

COPY postgresql-42.2.24.jar .

COPY src/ src/

COPY main.py .