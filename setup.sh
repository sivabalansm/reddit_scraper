#! /bin/bash
[ -e ./env ] || python -m venv env 
source ./env/bin/activate
pip install -r ./requirements.txt

