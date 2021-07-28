#!/bin/bash
docker build . -t "urunner:agent"
# docker run urunner:agent ping ls

docker run urunner:agent python3 app.py --add-host=host.docker.internal:host-gateway --network=host