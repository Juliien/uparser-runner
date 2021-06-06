#!/bin/bash
docker run --rm urunner # -v $(pwd)/output:/data/:rw
#docker logs -f urunner &> logs.txt
exit 0
# --rm cleanup after each run
# -v volume, to share a volume with host machine
