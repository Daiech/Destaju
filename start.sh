#!/bin/bash
uwsgi --socket :9091 --wsgi-file SGLC/wsgi.py -d service.log
