# syntax=docker/dockerfile:1

FROM python:3.11-bullseye
ENV PYTHONDONTWRITEBYTECODE 1

RUN ln -snf /usr/share/zoneinfo/Asia/Kuala_Lumpur /etc/localtime && echo Asia/Kuala_Lumpur > /etc/timezone

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    git \
    libssl-dev \
    libcurl4-openssl-dev \
    python3 \
    python3-dev \
    libmariadb-dev-compat \
    libmariadb-dev \
    cron \
    python3-pip \
    gunicorn

RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install eventlet

RUN mkdir /app
WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# CMD ["flask", "run"]
CMD /usr/local/bin/gunicorn -w 16 -b :5000 --worker-class eventlet --reload --threads=16 main:app