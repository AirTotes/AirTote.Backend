#!/bin/sh

export LANG=en_US.utf8

cd `dirname $0`

python3 ./GetMetarTaf/GetMetarTaf.py
