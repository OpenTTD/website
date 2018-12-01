#!/bin/sh

set -e

echo "Running test build for Docker image ..."
docker build --pull --no-cache --force-rm -t openttd/website:testrun . \
    && docker rmi openttd/website:testrun
