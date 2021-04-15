#General
SHELL := /bin/bash
APT=apt-get install -y

#Django
PYTHON=/usr/bin/python3
DATA=./back-end/eevie/fill_db.py
DJANGO=$(PYTHON) ./back-end/manage.py

#React
NPM=/usr/bin/npm

py_deps:


yarn_install: 
	sudo $(NPM) install --global yarn




