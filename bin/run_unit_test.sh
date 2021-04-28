#!/bin/bash

echo "Installing packages"
#pip3 install -r requirements.txt

echo "Running unit tests"
python3 -m pytest -x -v --color=yes tests/ --cov=home_automation_framework --cov-config bin/.coveragerc --cov-report term-missing -p no:warnings
rm .coverage
