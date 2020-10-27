#!/bin/bash
home_dir=$(pwd)

echo "Installing packages"
#pip3 install -r requirements.txt


echo "Running unit tests"
#python3 -m unittest discover -s tests/ -p 'test_*.py'


echo "Linting of src folder"
sub_dirs=("db"  "iot_gateway"  "logging")
for sub_dir in ${sub_dirs[*]}; do
  echo "Linting for src/$sub_dir"
  cd "$home_dir/src/$sub_dir" || { echo "cd error, check location"; exit 1; }
  pylint -j 2 --rcfile="$home_dir/.github/workflows/setup.cfg" --output-format=colorized `ls -R | grep .py$ | xargs`
done
cd "$home_dir" || { echo "cd error, check location"; exit 1; }


echo "Linting of lib folder"
cd "$home_dir/lib" || { echo "cd error, check location"; exit 1; }
pylint -j 2 --rcfile="$home_dir/.github/workflows/setup.cfg" --output-format=colorized `ls -R | grep .py$ | xargs`
cd "$home_dir" || { echo "cd error, check location"; exit 1; }