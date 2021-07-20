# syntax=docker/dockerfile:1
FROM ubuntu:20.04
WORKDIR /runner

# python requirements
RUN apt-get update && apt-get install --no-install-recommends -y python3.8 python3-pip python3.8-dev
COPY . .
RUN python3 -m pip install -r requirements.txt

# DEBUG redirect stdout and stderr to files
# RUN exec >/code/stdout.log
# RUN exec 2>/code/stderr.log
