FROM python:3.7.2-stretch

ENV LISTEN_PORT=5000
EXPOSE 5000

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY ./code /usr/src/app
CMD gunicorn --bind 0.0.0.0:8000 wsgi:app
