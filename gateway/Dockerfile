FROM python:3.12.0 as gateway

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN mkdir gateway

COPY . ./gateway

WORKDIR gateway

