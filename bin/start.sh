#!/bin/sh

uwsgi --socket 0.0.0.0:5000 --processes=4 --protocol=http --uid=root --master -w app:app