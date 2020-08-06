#!/bin/sh

PYTHONPATH=$(readlink -f src/) python -m discolight.mkreadme "$@"
