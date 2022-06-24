#!/bin/sh

GET_METAR_SH='GetNoaaMetar.sh'
GET_TAF_SH='GetNoaaTaf.sh'

export LANG=en_US.utf8

cd `dirname $0`

bash $GET_METAR_SH

bash $GET_TAF_SH
