#!/bin/sh

PYTHONPATH=$(readlink -f src/) pylint --rcfile=.pylintrc-non-codacy discolight | sort -u && flake8 src/ && pydocstyle --add-select=D203,D212,D205,D200 --add-ignore=D211 --match='(?!__init__).*\.py' src/
