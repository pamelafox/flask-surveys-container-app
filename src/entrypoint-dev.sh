#!/bin/sh
flask db upgrade && gunicorn -c gunicorn.conf.py --reload app:app
