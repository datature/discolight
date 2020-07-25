#!/bin/sh

PYTHONPATH=$(readlink -f src/) pylint --rcfile=.pylintrc-non-codacy discolight | sort -u && flake8 src/ && pep257 --match='(?!__init__).*\.py' src/
