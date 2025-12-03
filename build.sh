#!/usr/bin/env bash

pip install -r requirements.txt

cd metanit

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'password')" | python manage.py shell

python manage.py collectstatic --noinput

python manage.py migrate