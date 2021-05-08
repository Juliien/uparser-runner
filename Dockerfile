# syntax=docker/dockerfile:1
FROM python:3.8-alpine
WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN EXPORT="PYTHONPATH:=src/"
EXPOSE 5000
COPY . .
RUN echo "$PWD"
RUN ls
CMD ["flask", "run"]