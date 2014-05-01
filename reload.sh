#!/bin/bash
ps -Af | grep uwsgi | grep -v grep | grep 9091 | awk '{ print $2 }' | xargs kill
echo Stopped...
echo Wait...
sleep 1
uwsgi --socket :9091 --wsgi-file SGLC/wsgi.py -d service.log
echo Started...




