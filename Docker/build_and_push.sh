#!/bin/sh
NAME="home_automation_framework"
TAG="v0.1"
SHORT_NAME=$NAME:$TAG
DOCKER_REPO="dankersw/"$SHORT_NAME

echo "Building docker image"
docker build --build-arg TAG=$TAG -t $SHORT_NAME ..

echo "Tagging for local registry and pushing image/tags"
docker tag $SHORT_NAME $DOCKER_REPO
docker push $DOCKER_REPO
docker rmi $SHORT_NAME
