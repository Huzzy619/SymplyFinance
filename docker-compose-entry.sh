#!/bin/sh

echo "Migrating data"
python3 manage.py migrate

echo "Starting server"
python3 manage.py runserver 0.0.0.0:8000