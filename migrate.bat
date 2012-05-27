@echo off
python manage.py schemamigration blogsadmin --auto
python manage.py schemamigration doorsadmin --auto
python manage.py migrate blogsadmin
python manage.py migrate doorsadmin
