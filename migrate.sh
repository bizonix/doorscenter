#!/bin/bash
python manage.py schemamigration doorsadmin --auto
python manage.py migrate doorsadmin

python manage.py schemamigration sapeadmin --auto
python manage.py migrate sapeadmin
