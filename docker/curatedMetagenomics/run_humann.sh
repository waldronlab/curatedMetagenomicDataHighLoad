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
    --taxonomic-profile metaphlan_bugs_list/${sample}.tsv \
    --protein-database ${unirefdir} \
    --metaphlan-options '--bowtie2db $metaphlandb' \
    --threads=${ncores}

mkdir genefamilies genefamilies_relab pathabundance pathabundance_relab pathcoverage

mv humann/${sample}_genefamilies.tsv genefamilies/${sample}.tsv
mv humann/${sample}_pathabundance.tsv pathabundance/${sample}.tsv
mv humann/${sample}_pathcoverage.tsv pathcoverage/${sample}.tsv

humann_renorm_table \
    --input genefamilies/${sample}.tsv \
    --output genefamilies_relab/${sample}.tsv \
    --units relab

humann_renorm_table \
    --input pathabundance/${sample}.tsv \
    --output pathabundance_relab/${sample}.tsv \
    --units relab
