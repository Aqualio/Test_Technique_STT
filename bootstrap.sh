#!/bin/sh

export FLASK_APP=./STT/STT_index.py

pipenv run flask --debug run -h 0.0.0.0