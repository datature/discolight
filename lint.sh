#!/bin/sh

PYTHONPATH=$(readlink -f src/) pylint --rcfile=.pylintrc discolight | sort -u && flake8 src/
