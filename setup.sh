#! /bin/bash
ROOT=$1
[ -z "$ROOT" ] && ROOT="." && echo "making $(pwd) root"
[ -e $ROOT/env ] || python -m venv env 
source $ROOT/env/bin/activate
pip install -r $ROOT/requirements.txt

