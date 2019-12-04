#!/bin/bash

cd /app/projectq_server
ls
env
python3 manage.py runserver 0.0.0.0:8000

echo "container started " > /var/log/run.log
tail -f /var/log/run.log
