#!/bin/sh

export LANG=en_US.utf8

cd `dirname $0`

/usr/local/bin/python3 ./GetMetarTaf/GetMetarTaf.py
