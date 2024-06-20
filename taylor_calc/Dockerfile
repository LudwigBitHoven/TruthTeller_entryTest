FROM python:3.12.0 as taylor_calc

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN mkdir taylor_calc

COPY . ./taylor_calc

WORKDIR taylor_calc

