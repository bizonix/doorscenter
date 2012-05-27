#!/bin/bash
git pull origin master
python manage.py migrate blogsadmin
python manage.py migrate doorsadmin
