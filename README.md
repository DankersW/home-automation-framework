![home_server tests](https://github.com/DankersW/Home_Automation/workflows/home_server_tests/badge.svg)
# Home Automation framework
Handles all the communication between my IoT units. It also acts as the link between GCP and my home appliances. 
All IoT units needs to go through the gateway to access the internet. There is one MQTT IoT gateway handling IoT 
traffic. In the future more IoT gateways will be added to handle addition communication protocols
An addition MQTT gateway is present handling traffic going to and from GPC. 

## Architecture
![Architecture](resources/images/architecture_home_automation.png "Architectural overview")
Architectural design made via  [Lucidchart](https://app.lucidchart.com/documents/edit/2025f710-b9e7-49ac-844c-e21cea54473a/0_0)

## Run
```bash
pip3 install -r requirements.txt
python3 server.py
```