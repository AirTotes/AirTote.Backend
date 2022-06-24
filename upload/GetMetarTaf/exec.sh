#!/bin/sh

GET_METAR_SH='GetNoaaMetar.sh'

export LANG=en_US.utf8

cd `dirname $0`

bash $GET_METAR_SH
