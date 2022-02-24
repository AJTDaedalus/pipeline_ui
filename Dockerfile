FROM python:3.7.2-stretch

ENV LISTEN_PORT=5000
EXPOSE 5000

WORKDIR /code

COPY ./requirements.txt /code
RUN pip install -r requirements.txt

COPY ./code /code
CMD python main.py
