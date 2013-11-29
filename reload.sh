#!/bin/bash
ps -Af | grep uwsgi | grep -v grep | awk '{ print $2 }' | xargs kill
echo Stopped...
echo Wait...
sleep 1
uwsgi --socket :8001 --wsgi-file sglcWsgi.py -d service.log
echo Started...




