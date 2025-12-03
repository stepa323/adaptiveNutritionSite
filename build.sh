#!/usr/bin/env bash

pip install -r requirements.txt

cd metanit

python manage.py collectstatic --noinput

python manage.py migrate