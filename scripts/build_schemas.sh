#!/bin/bash

PYTHON=${1:-"/usr/bin/env python"}

if [ ! $VIRTUAL_ENV ]
then
    echo "Must be running inside virtualenv! Please see https://virtualenv.pypa.io/en/stable/userguide/"
    exit -1
fi

pip show mediachain-client 2>&1 > /dev/null
if [ $? -eq 1 ]
then
    echo "Requirements not installed, installing..."
    pip install .
fi

pip install -U --no-deps --no-cache-dir -q .
python setup.py test

if [ $? -ne 0 ]
then
    echo "Tests failed, not publishing"
    exit $?
fi

python setup.py publish_translators

