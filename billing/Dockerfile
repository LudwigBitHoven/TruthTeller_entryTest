FROM python:3.12.0 as billing

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN mkdir billing

COPY . ./billing

WORKDIR billing

