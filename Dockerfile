FROM python:3.6

ENV LISTEN_PORT=5000
EXPOSE 5000

WORKDIR /code

COPY ./requirements.txt /code
RUN pip install -r requirements.txt

COPY ./code /code
CMD python main.py
