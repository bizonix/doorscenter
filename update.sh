#!/bin/bash
git pull origin master
python manage.py migrate doorsadmin
python manage.py migrate sapeadmin
