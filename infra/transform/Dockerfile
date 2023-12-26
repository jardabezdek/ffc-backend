# Using image phidata/duckdb:0.9.2, because of duckdb error described here:
# https://github.com/duckdb/duckdb/issues/8035#issuecomment-1814518133

FROM phidata/duckdb:0.9.2 as python-base
MAINTAINER Jaroslav Bezdek

RUN apt-get --allow-releaseinfo-change update

RUN apt-get install -y build-essential \
  python3-dev \
  python3-pip \
  python3-venv

# install python requirements
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

# load environment variables from .env file
COPY .env .
RUN set -a && source .env && set +a

WORKDIR /usr/src/app

ENV PYTHONPATH=/usr/src/app
