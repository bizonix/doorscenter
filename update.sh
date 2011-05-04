#!/bin/bash
git pull origin master
python manage.py migrate doorsadmin
sudo /etc/init.d/apache2 reload
