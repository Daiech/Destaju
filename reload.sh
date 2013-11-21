#!/bin/bash
ps -Af | grep uwsgi | grep -v grep | awk '{ print $2 }' | xargs kill
uwsgi --socket :8001 --wsgi-file sglcWsgi.py -d service.log