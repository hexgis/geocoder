

FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV C_INCLUDE_PATH=/usr/include/gdal 
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal

RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN apt-get update
RUN apt-get install libgdal-dev --yes 
RUN pip install pip --upgrade
RUN pip install -r requirements.txt
