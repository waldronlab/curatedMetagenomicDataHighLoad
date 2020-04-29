#!/bin/bash

## Usage:
# export metaphlandb=${HOME}/biobakery_databases/humann/chocophlan
# download_metaphlandb.sh

mkdir -p $metaphlandb
metaphlan --install --index mpa_v20_m200 --bowtie2db $metaphlandb
