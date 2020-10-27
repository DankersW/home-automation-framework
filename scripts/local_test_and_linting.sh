#!/bin/bash

echo "Running unit tests"
pwd
coverage run -m unittest discover -s tests/ -p 'test_*.py'

#coverage run -m unittest discover -s tests/ -p 'test_*.py'