#!/bin/bash
python manage.py schemamigration doorsadmin --auto
python manage.py migrate doorsadmin
