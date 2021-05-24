FROM ubuntu:20.04

WORKDIR /home-automation-framework

RUN apt update && apt install -y python3.8 python3-pip

COPY requirements.txt .
COPY home_automation_framework home_automation_framework/.
COPY home_automation_framework.py .
COPY docker/configuration.yml .
COPY docker/entrypoint.sh .

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "sh", "entrypoint.sh" ]
