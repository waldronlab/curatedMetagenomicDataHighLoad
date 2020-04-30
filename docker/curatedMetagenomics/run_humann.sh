#!/bin/bash

## Usage:
# export metaphlandb=${HOME}/biobakery_databases/humann/chocophlan
# export chocophlandir=/usr/local/humann_databases/chocophlan
# export unirefdir=/usr/local/humann_databases/uniref
# run_humann.sh $sample $ncores

sample=$1
ncores=$2

humann \
    --input reads/${sample}.fastq \
    --output humann \
    --nucleotide-database ${chocophlandir} \
    --taxonomic-profile metaphlan/${sample}.tsv \
    --protein-database ${unirefdir} \
    --metaphlan-options '--bowtie2db $metaphlandb'
    --threads=${ncores}

humann_renorm_table --input humann/${sample}_genefamilies.tsv --output humann/${sample}_genefamilies_relab.tsv --units relab
humann_renorm_table --input humann/${sample}_pathabundance.tsv --output humann/${sample}_pathabundance_relab.tsv --units relab
