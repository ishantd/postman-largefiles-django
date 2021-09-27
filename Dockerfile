# pull official base image
FROM ubuntu:latest

# set work directory
RUN mkdir /code
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN apk add --no-cache --update \
#     python3 python3-dev gcc \
#     gfortran musl-dev g++ \
#     libffi-dev openssl-dev \
#     libxml2 libxml2-dev \
#     libxslt libxslt-dev \
#     libjpeg-turbo-dev zlib-dev \
#     libsodium-dev build-base libzmq musl-dev zeromq-dev

# # install psycopg2 dependencies
# RUN apk update \
#     && apk add postgresql-dev gcc python3-dev musl-dev

RUN apt-get update \
    && apt-get -y install libpq-dev python3-pip python3-dev python3-venv gcc \
    && pip install psycopg2

RUN apt install default-jre

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install wheel
RUN \ 
    pip3 install --no-cache-dir Cython
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY entrypoint.sh /code/
RUN sed -i 's/\r$//g' /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

# copy project
COPY . /code/

# run entrypoint.sh
ENTRYPOINT ["sh", "/code/entrypoint-2.sh"]