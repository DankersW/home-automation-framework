# Docker
Some simple documentation about building and pushing the docker image

## Build
```bash
docker build -t home_automation_framework .
```

## Push to docker hub
```bash
docker tag home_automation_framework:latest dankersw/home_automation_framework:latest
docker push dankersw/home_automation_framework:latest
```

One liner for development purposes
```bash
tag=0.1 && docker build -t home_automation_framework . && docker tag home_automation_framework:latest dankersw/home_automation_framework:$tag && docker push dankersw/home_automation_framework:$tag

```
