#!/bin/bash
ps aux | grep manage | sed 's/\s\+/ /g' | cut -f2 -d' ' | head -n1 | xargs kill -9
pip install -r requirements.txt
./manage.py migrate
./manage.py runfcgi method=threaded host=127.0.0.1 port=3033
# eralchemy -i 'postgresql+psycopg2://postgres:postgres@localhost:5432/harnas' -o filtered.pdf
