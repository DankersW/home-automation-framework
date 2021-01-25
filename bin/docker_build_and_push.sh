#!/bin/sh
IMAGE_NAME="home_automation_framework"
DOCKER_USR="dankersw"
TAG="0.2"
NAME=$IMAGE_NAME:$TAG
DOCKER_REPO=$DOCKER_USR/$NAME

echo "Building docker image"
docker build --build-arg TAG=$TAG -t $NAME ..

echo "Tagging for local registry and pushing image/tags"
docker tag $NAME $DOCKER_REPO
docker push $DOCKER_REPO
docker rmi $NAME
