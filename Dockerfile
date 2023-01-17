FROM python:latest

WORKDIR /code

RUN pip install requests
COPY ./src/ ./

CMD python -u main.py