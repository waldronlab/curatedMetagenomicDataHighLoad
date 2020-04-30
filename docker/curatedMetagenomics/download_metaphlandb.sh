#!/bin/bash

## Usage:
# export metaphlandb=${HOME}/biobakery_databases/humann/chocophlan
# download_metaphlandb.sh

mkdir -p $metaphlandb
metaphlan --install --index latest --bowtie2db $metaphlandb
