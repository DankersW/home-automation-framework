![framework_unit_tests](https://github.com/DankersW/Home_Automation/workflows/framework_unit_tests/badge.svg) [![codecov](https://codecov.io/gh/DankersW/home-automation-framework/branch/master/graph/badge.svg?token=FJDSUMMWO0)](https://codecov.io/gh/DankersW/home-automation-framework) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/14720ee94823416288382efe00e56ed7)](https://www.codacy.com/gh/DankersW/home-automation-framework/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=DankersW/home-automation-framework&amp;utm_campaign=Badge_Grade)
# Home Automation framework
Handles all the communication between my IoT units. It also acts as the link between GCP and my home appliances. 
All IoT units needs to go through the gateway to access the internet. There is one MQTT IoT gateway handling IoT 
traffic. In the future more IoT gateways will be added to handle addition communication protocols
An addition MQTT gateway is present handling traffic going to and from GPC. 

## Architecture
![Architecture](docs/static/images/Home-automation-framework.png "Architectural overview")
Architectural design made via  [Lucidchart](https://lucid.app/lucidchart/dbce786e-f6e2-41f7-8d71-51f903208ce9/edit?page=0_0#?folder_id=home&browser=icon)

## Run
Run the docker-compose file located at [home-automation](https://github.com/DankersW/home-automation)

```bash
pip3 install -r requirements.txt
python3 home_automation_framework.py
```
