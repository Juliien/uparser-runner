#!/bin/bash
docker build . -t "urunner:agent"
docker run urunner:agent ./app.py