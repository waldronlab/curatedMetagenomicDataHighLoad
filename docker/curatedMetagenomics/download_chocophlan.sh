#!/bin/bash

## Usage (argument is optional, default is dropbox)
# export chocophlandir=${HOME}/biobakery_databases/humann/chocophlan
# download_chocophlan.sh dropbox
# download_chocophlan.sh google
# download_chocophlan.sh harvard
# download_chocophlan.sh gsutil

if [ -z ${chocophlandir} ]; then
    echo '$chocophlandir environment variable must be set'
    exit 1
fi

if [ -z $1 ]; then
    dbsource="dropbox"
else
    dbsource=$1
fi

## figure out URLs by doing `humann3_databases`

chocophlanname="full_chocophlan.v296_201901.tar.gz"

if [ ${dbsource} == 'dropbox' ]; then
    chocophlanurl="https://www.dropbox.com/s/das8hdof0zyuyh8/${chocophlanname}?dl=1"
fi

if [ ${dbsource} == 'harvard' ]; then
    chocophlanurl="http://huttenhower.sph.harvard.edu/humann2_data/chocophlan/${chocophlanname}"
fi

if [ ${dbsource} == 'google' ]; then
    chocophlanurl="https://storage.googleapis.com/humann2_data/${chocophlanname}"
fi

if [ ${dbsource} == 'gsutil']; then
    gsutil cp gs://humann2_data/${chocophlanname} .
else
    wget $chocophlanurl
fi

tar -xvz -C $chocophlandir -f $chocophlanname
rm $chocophlanname
