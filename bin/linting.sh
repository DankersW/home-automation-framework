#!/bin/bash
home_dir=$(pwd)

echo "Linting of home_automation_framework folder"
sub_dirs=("db"  "iot_gateway"  "logging" "host_health" "framework" "utils")
for sub_dir in ${sub_dirs[*]}; do
  echo "Linting for src/$sub_dir"
  cd "$home_dir/home_automation_framework/$sub_dir" || { echo "cd error, check location"; exit 1; }
  pylint -j 2 --rcfile="$home_dir/.github/workflows/setup.cfg" --output-format=colorized $(ls -R | grep .py$ | xargs)
done
cd "$home_dir" || { echo "cd error, check location"; exit 1; }
