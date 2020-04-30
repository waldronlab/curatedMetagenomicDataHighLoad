#!/bin/bash

## Usage:
# export metaphlandb=${HOME}/biobakery_databases/humann/chocophlan
# run_metaphlan.sh $sample $ncores

sample=$1
ncores=$2

metaphlan \
    --input_type fastq \
    --index latest \
    --bowtie2db ${metaphlandb} \
    --samout metaphlan/${sample}.sam \
    --bowtie2out metaphlan/${sample}.bowtie2out \
    --nproc ${ncores} \
    -o metaphlan/${sample}.tsv \
    reads/${sample}.fastq

metaphlan \
    --input_type bowtie2out \
    --index latest \
    --bowtie2db ${metaphlandb} \
    -t marker_pres_table \
    -o metaphlan/${sample}.marker_pres_table \
    metaphlan/${sample}.bowtie2out

metaphlan \
    --input_type bowtie2out \
    --index latest \
    --bowtie2db ${metaphlandb} \
    -t marker_ab_table \
    -o metaphlan/${sample}.marker_ab_table \
    metaphlan/${sample}.bowtie2out