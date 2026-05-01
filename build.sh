#!/usr/bin/env bash
set -o errexit  

pip install -r requirements.txt
sudo apt-get install -y gettext   
python manage.py compilemessages 
python manage.py collectstatic --noinput
python manage.py migrate