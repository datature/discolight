#!/bin/sh

PYTHONPATH=$(readlink -f src) coverage run -m pytest "$@" && coverage xml -o cobertura.xml
