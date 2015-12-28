#!/bin/bash
kill `cat harnas.pid`
rm -f harnas.pid
pip install -r requirements.txt
./manage.py migrate
./manage.py runfcgi method=threaded host=127.0.0.1 port=3033 daemonize=$HARNAS_DAEMONIZE pidfile=harnas.pid
# eralchemy -i 'postgresql+psycopg2://postgres:postgres@localhost:5432/harnas' -o filtered.pdf
