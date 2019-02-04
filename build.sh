#!/bin/sh

set -xe

VERSION=$(git rev-parse HEAD)
TAG=$(git describe --tags 2>/dev/null || echo $VERSION)

docker build -t minions:${TAG} -t minions:latest --build-arg version=${VERSION} .
