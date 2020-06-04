#!/bin/bash

### usage: bash curatedMetagenomicData_pipeline.sh sample_name "SRRxxyxyxx;SRRyyxxyyx"
### If third argument is "DEMO" a test will be done.

### example of running docker and singularity. 
## Set environment variables
# OUTPUT_PATH=$(pwd)            # default is $(pwd)
# ncores=2                      # default is 2
# DB_PATH=${HOME}/biobakery.db  # only for mounting persistent database volume for Docker, otherwise databases written only within Docker container

## Docker:
# mkdir -p $DB_PATH
# docker run -it -e OUTPUT_PATH=${OUTPUT_PATH} -e ncores=${ncores} -v ${DB_PATH}/metaphlan:/usr/local/miniconda3/lib/python3.7/site-packages/metaphlan/metaphlan_databases -v ${DB_PATH}/humann:/usr/local/humann_databases waldronlab/curatedmetagenomics

## Singularity - note, the binding here does not actually allow you to write anything to /usr/local, 
##     which will be a problem for database downloads if not using DEMO example. I don't yet have a fix for this.
# singularity pull docker://waldronlab/curatedmetagenomics
# mkdir -p $DB_PATH
# singularity shell -B ${DB_PATH}/metaphlan:/usr/local/miniconda3/lib/python3.7/site-packages/metaphlan/metaphlan_databases -B ${DB_PATH}/humann:/usr/local/humann_databases curatedmetagenomics_latest.sif

## Now run a demo
# curatedMetagenomicData_pipeline.sh demosamplename SRR042612 DEMO

### before running this script, be sure that these tools are in your path
# fasterq-dump
# humann3
# metaphlan
# python

sample=$1
runs=$2
if [ -z ${3} ]
then
    run_demo=FALSE
else
    run_demo=$3
fi

if [ -z ${ncores} ]
then
    ncores=2
fi

if [ -z ${OUTPUT_PATH} ]
then
    OUTPUT_PATH=$(pwd)
fi

### the default metaphlan directory is set by the $mpa_dir environment variable
### in the waldronlab/curatedmetagenomics docker container this is:
### /usr/local/miniconda3/lib/python3.7/site-packages/metaphlan
### MetaPhlAn databases can be downloaded by running 
### metaphlan --install --index mpa_v20_m200
if [ -z ${metaphlandb} ]
then
    echo '$metaphlandb environment variable must be set. Exiting.'
    exit 1
fi

### Set a location for the humann data directory
### This script assumes the humann data directory is set by the $humanndb environment variable
### in the waldronlab/curatedmetagenomics docker container this is:
### /usr/local/humann_databases
if [ -z ${humanndb} ]
then
    echo '$humanndb environment variable must be set. Exiting.'
    exit 1
fi

if [ -z ${metaphlandb} ]
then
    echo '$metaphlandb environment variable must be set. Exiting.'
    exit 1
fi

if [ -z ${chocophlandir} ]
then
    echo '$chocophlandir environment variable must be set. Exiting.'
    exit 1
fi

if [ -z ${unirefdir} ]
then
    echo '$unirefdir environment variable must be set. Exiting.'
    exit 1
fi

## For testing purposes, use the reduced ChocoPhlAn and UniRef90 DEMO databases
## A small fastq will be downloaded and profiled
if [ ${run_demo} == 'DEMO' ]
then
    DEMO_unirefname="uniref90_DEMO_diamond_v201901.tar.gz"
    DEMO_unirefurl="https://www.dropbox.com/s/xaisk05u4l822pl/uniref90_DEMO_diamond_v201901.tar.gz?dl=1" ##
    DEMO_chocophlanname="DEMO_chocophlan.v296_201901.tar.gz"
    DEMO_chocophlanurl="https://www.dropbox.com/s/66wgnzw0eo1z142/DEMO_chocophlan.v296_201901.tar.gz?dl=1" ##

    wget $DEMO_unirefurl -O $DEMO_unirefname
    tar -xvzf $DEMO_unirefname -C $unirefdir
    rm $DEMO_unirefname
    
    wget $DEMO_chocophlanurl -O $DEMO_chocophlanname
    tar -xvzf $DEMO_chocophlanname -C $chocophlandir 
    rm $DEMO_chocophlanname
    sample='DEMO'
fi

echo "Working in ${OUTPUT_PATH}"
mkdir -p ${OUTPUT_PATH}

cd ${OUTPUT_PATH}

for run in ${runs//;/ }
do
    echo 'Dumping run '${run}
    fasterq-dump --threads ${ncores} --split-files ${run} --outdir reads
    echo 'Finished downloading of run '${run}
done
echo 'Downloaded.'

echo 'Concatenating runs...'
if [ ${sample} == 'DEMO' ]
then
    mkdir -p reads
    cat $hnn_dir/tests/data/demo.fastq > reads/${sample}.fastq
else
    cat reads/*.fastq > reads/${sample}.fastq
fi

mkdir -p metaphlan
if [ -e reads/${sample}.fastq ]
then
    echo 'Running metaphlan'
    run_metaphlan.sh ${sample} ${ncores}
else
    echo 'MetaPhlAn execution has failed. Cannot find the input metagenome. Exiting.'
    exit 1
fi

if [ -e metaphlan/${sample}.sam.bz2 ]
then
    echo 'Running strainphlan'
    run_strainphlan.sh ${sample} ${ncores}
else
    echo 'MetaPhlAn execution has failed. StrainPhlAn can not be executed. Exiting.'
    exit 1
fi

mkdir -p humann
echo 'Running humann'
if [ -e metaphlan_bugs_list/${sample}.tsv ]
then
    run_humann.sh $sample $ncores
else
    echo 'MetaPhlAn execution has failed. HUMAnN can not be executed. Exiting.'
    exit 2
fi

mkdir humann_temp; mv humann/${sample}_humann_temp/ humann_temp/ #comment this line if you don't want to keep humann temporary files
rm -r humann
rm -r reads