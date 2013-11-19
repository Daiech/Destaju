#!/bin/bash

uwsgi --socket :8001 --wsgi-file sglcWsgi.py -d service.log
