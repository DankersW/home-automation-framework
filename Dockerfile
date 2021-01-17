FROM ubuntu:20.04

WORKDIR /home-automation-framework

RUN apt update && apt install -y python3.8

COPY requirements.txt .
COPY home_automation_framework .

#RUN pip3 install -r requirements.txt

#CMD [ "python3", "./home_automation_framework.py" ]
