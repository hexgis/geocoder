### STAGE 1: Build GDAL ###
FROM geodata/gdal:2.1.3
RUN gdalinfo --version

### STAGE 2: Install requirements
FROM python:3

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update && apt-get install --yes libgdal-dev
RUN pip install -r requirements.txt
COPY . /code/
