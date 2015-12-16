#!/bin/bash
pip install -r requirements.txt
./manage.py syncdb
./manage.py runfcgi method=threaded host=127.0.0.1 port=3033