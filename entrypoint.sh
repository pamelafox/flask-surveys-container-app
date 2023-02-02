#!/bin/sh
flask db upgrade && gunicorn -c gunicorn.conf.py app:app
