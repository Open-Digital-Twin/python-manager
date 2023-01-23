FROM python:latest

WORKDIR /code

RUN pip install requests
RUN pip install kubernetes
COPY ./src/ ./

CMD python -u main.py