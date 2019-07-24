FROM python:3.7
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
