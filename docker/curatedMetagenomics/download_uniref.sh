#!/bin/bash

## Usage (argument is optional, default is dropbox)
# unirefdir=${HOME}/biobakery_databases/humann/uniref
# download_uniref.sh dropbox
# download_uniref.sh google
# download_uniref.sh harvard
# download_uniref.sh gsutil

if [ -z ${unirefdir} ]; then
    echo '$unirefdir environment variable must be set'
    exit 1
fi

if [ -z $1 ]; then
    dbsource="dropbox"
else
    dbsource=$1
fi


## figure out URLs by doing `humann3_databases`

unirefname="uniref90_annotated_v201901.tar.gz"

if [ ${dbsource} == 'dropbox' ]; then
    unirefurl="https://www.dropbox.com/s/yeur7nm7ej7spga/${unirefname}?dl=1"
fi

if [ ${dbsource} == 'harvard' ]; then
    unirefurl="http://huttenhower.sph.harvard.edu/humann2_data/uniprot/uniref_annotated/${unirefname}"
fi

if [ ${dbsource} == 'google' ]; then
    unirefurl="https://storage.googleapis.com/humann2_data/${unirefname}"
fi

if [ ${dbsource} == 'gsutil']; then
    gsutil cp gs://humann2_data/${unirefname} .
else
    wget $unirefurl
fi

tar -xvz -C $unirefdir -f $unirefname
rm $unirefname
