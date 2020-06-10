#!/bin/bash

## Usage (environment variable must be set before running the script)
# export chocophlandir=${HOME}/biobakery_databases/humann/chocophlan
# export chocophlanname="full_chocophlan.v296_201901.tar.gz"
# export chocophlanurl="https://www.dropbox.com/s/das8hdof0zyuyh8/${chocophlanname}?dl=1"
# download_chocophlan.sh

if [ -z ${chocophlandir} ]; then
    echo '$chocophlandir environment variable must be set'
    exit 1
fi

mkdir -p $chocophlandir

if [ -z ${chocophlanname} ] || [ -z ${chocophlanurl} ]
then
    echo '$chocophlanname and $chocophlanurl environment variables must be set. Exiting.'
    exit 1
fi

if [[ $chocophlanurl =~ "https://storage.googleapis.com" ]] && [ ! -z $(command -v gsutil) ]
then
    gsutil cp gs://humann2_data/${chocophlanname} .
else
    wget ${chocophlanurl} -O ${chocophlanname}
fi

tar -xvz -C $chocophlandir -f $chocophlanname
rm $chocophlanname
