# syntax=docker/dockerfile:1
FROM alpine:3.7
WORKDIR /code

# python requirements
# COPY requirements.txt requirements.txt
# RUN python3 -m pip install -r requirements.txt
# RUN EXPORT="PYTHONPATH:=`pwd`"

CMD echo "Starting Urunner"; sleep 10; echo "Terminating Urunner"