# pull the official base image
FROM python:3.8.3-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip 
COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt

# Install psycopg2
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# copy project
COPY . /usr/src/app

# Expose Port
EXPOSE 8888

# Start with gunicorn
CMD ["gunicorn", "--chdir", "api", "--bind", ":8888", "api.wsgi:application"]