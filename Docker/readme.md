# Docker


## Build
```bash
docker build -t home_automation_framework .
```

## Push to docker hub
```bash
docker tag home_automation_framework:latest dankersw/home_automation_framework:latest
docker push dankersw/home_automation_framework:latest
```