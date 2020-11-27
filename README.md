![home_server tests](https://github.com/DankersW/Home_Automation/workflows/home_server_tests/badge.svg)
# Home Automation framework

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6da0dcf4b38a4ab0af6d42debb5227a3)](https://app.codacy.com/gh/DankersW/home-automation-framework?utm_source=github.com&utm_medium=referral&utm_content=DankersW/home-automation-framework&utm_campaign=Badge_Grade)

Handles all the communication between my IoT units. It also acts as the link between GCP and my home appliances. 
All IoT units needs to go through the gateway to access the internet. There is one MQTT IoT gateway handling IoT 
traffic. In the future more IoT gateways will be added to handle addition communication protocols
An addition MQTT gateway is present handling traffic going to and from GPC. 

## Architecture
![Architecture](static/images/Home-automation-framework.png "Architectural overview")
Architectural design made via  [Lucidchart](https://lucid.app/lucidchart/dbce786e-f6e2-41f7-8d71-51f903208ce9/edit?page=0_0#?folder_id=home&browser=icon)

## Run
```bash
pip3 install -r requirements.txt
python3 server.py
```