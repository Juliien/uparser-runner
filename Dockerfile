# syntax=docker/dockerfile:1
FROM ubuntu:20.04
WORKDIR /agent

# python requirements
RUN apt-get update && apt-get install --no-install-recommends -y python3.8 python3-pip python3.8-dev python3-pip
COPY . .
RUN python3 -m pip install -r requirements.txt

EXPOSE 9092

RUN ls

WORKDIR /agent/urunner
# DEBUG redirect stdout and stderr to files
# RUN exec >/code/stdout.log
# RUN exec 2>/code/stderr.log
