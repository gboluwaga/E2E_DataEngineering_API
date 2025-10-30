ARG AIRFLOW_VERSION=2.9.2
ARG PHYTON_VERSION=3.10


FROM apache/airflow:${AIRFLOW_VERSION}-python${PHYTON_VERSION}

ENV AIRFLOW_HOME =/opt/airflow

COPY requirements.txt /

RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt