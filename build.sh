#!/bin/sh

set -xe

VERSION=$(git rev-parse HEAD)
TAG=$(git describe --tags 2>/dev/null || echo $VERSION)

docker build -t posipaky.info:latest -t hub:5000/posipaky.info:latest --build-arg version=${VERSION} .
