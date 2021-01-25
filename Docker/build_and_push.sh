#!/bin/sh
set -e
REG_HOST="esw-artifactory.got.volvo.net"
NAME="ocp-webhook"
TAG=$(git describe --always)
SHORT_NAME=$NAME:$TAG
FULL_NAME=$REG_HOST:5000/$SHORT_NAME
cd .. # Hacky solution to solve include paths in the docker file
docker build --build-arg TAG=$TAG -t $SHORT_NAME -f docker/Dockerfile .
echo "Tagging for local registry and pushing image/tags"
docker tag $SHORT_NAME $FULL_NAME

docker login -u "${artifactory_api_username}" -p "${artifactory_api_key}" $REG_HOST:5000

docker push $FULL_NAME
docker rmi $SHORT_NAME
