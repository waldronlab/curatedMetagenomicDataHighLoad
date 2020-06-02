#!/bin/bash

## Usage (environment variable must be set before running the script)
# export unirefdir=${HOME}/biobakery_databases/humann/uniref
# export unirefname="uniref90_annotated_v201901.tar.gz"
# export unirefurl="https://www.dropbox.com/s/yeur7nm7ej7spga/${unirefname}?dl=1"
# download_uniref.sh

if [ -z ${unirefdir} ]; then
    echo '$unirefdir environment variable must be set'
    exit 1
fi

mkdir -p $unirefdir

if [ -z ${unirefname} ] || [ -z ${unirefurl} ]
then
    echo '$unirefname and $unirefurl environment variables must be set. Exiting.'
    exit 1
fi

if [[ $unirefurl =~ "https://storage.googleapis.com" ]] && [ ! -z $(command -v gsutil) ]
then
    gsutil cp gs://humann2_data/${unirefname} .
else
    wget ${unirefurl} -O ${unirefname}
fi

tar -xvz -C $unirefdir -f $unirefname
rm $unirefname
