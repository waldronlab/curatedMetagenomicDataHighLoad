#!/bin/bash

## Usage:
# export metaphlandb=${HOME}/biobakery_databases/humann/chocophlan
# download_metaphlandb.sh


if [ -z ${metaphlandb} ]; then
    echo '$metaphlandb environment variable must be set'
    exit 1
fi

mkdir -p $metaphlandb
metaphlan --install --index latest --bowtie2db $metaphlandb
