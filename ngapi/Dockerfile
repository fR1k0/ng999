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
    gunicorn \
    unixodbc \
    unixodbc-dev \
    freetds-dev


RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install eventlet

RUN mkdir /rtapi
WORKDIR /rtapi

COPY . .
RUN pip install -r requirements.txt
RUN pip install uvicorn

# CMD ["python3", "app.py"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8888", "--reload"]