@echo off
python manage.py schemamigration doorsadmin --auto
python manage.py migrate doorsadmin
