#!/bin/bash

## Usage:
# export metaphlandb=${HOME}/biobakery_databases/humann/chocophlan
# run_strainphlan.sh $sample $ncores

sample=$1
ncores=$2

sample2markers.py -i metaphlan/${sample}.sam.bz2 \
    -o strainphlan \
    -n ${ncores}