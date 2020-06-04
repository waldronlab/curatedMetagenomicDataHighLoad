#!/bin/bash

## Usage:
# export metaphlandb=${HOME}/biobakery_databases/humann/chocophlan
# run_metaphlan.sh $sample $ncores

sample=$1
ncores=$2

mkdir marker_abundance marker_presence metaphlan_bugs_list

metaphlan \
    --input_type fastq \
    --index latest \
    --bowtie2db ${metaphlandb} \
    --samout metaphlan/${sample}.sam.bz2 \
    --bowtie2out metaphlan/${sample}.bowtie2out \
    --nproc ${ncores} \
    -o metaphlan_bugs_list/${sample}.tsv \
    reads/${sample}.fastq

metaphlan \
    --input_type bowtie2out \
    --index latest \
    --bowtie2db ${metaphlandb} \
    -t marker_pres_table \
    -o marker_presence/${sample}.tsv \
    metaphlan/${sample}.bowtie2out

metaphlan \
    --input_type bowtie2out \
    --index latest \
    --bowtie2db ${metaphlandb} \
    -t marker_ab_table \
    -o marker_abundance/${sample}.tsv \
    metaphlan/${sample}.bowtie2out