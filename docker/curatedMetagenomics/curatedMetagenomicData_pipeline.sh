#!/bin/bash

### usage: bash curatedMetagenomicData_pipeline.sh sample_name "SRRxxyxyxx;SRRyyxxyyx"
### For testing usage: bash curatedMetagenomicData_pipeline.sh DEMO SRR042612 DEMO

### before running this script, be sure that these tools are in your path
# fastq-dump
# humann3
# metaphlan
# python

sample=$1
runs=$2
run_demo=$3

### example docker command:
# OUTPUT_PATH=/nobackup/16tb_b/aaa
# docker run -it -e OUTPUT_PATH=$OUTPUT_PATH -v /nobackup/16tb_b/biobakery.db/metaphlan:/usr/local/miniconda3/lib/python3.7/site-packages/metaphlan/metaphlan_databases -v /nobackup/16tb_b/biobakery.db/humann:/usr/local/humann_databases waldronlab/curatedmetagenomics

### the default metaphlan directory is set by the $mpa_dir environment variable
### in the waldronlab/curatedmetagenomics docker container this is:
### /usr/local/miniconda3/lib/python3.7/site-packages/metaphlan
### MetaPhlAn databases can be downloaded by running 
### metaphlan --install --index mpa_v20_m200
### The previous command install the MetaPhlAn2 database
metaphlandb="${mpa_dir}/metaphlan_databases"

### Set a location for the humann data directory
### This script assumes the humann data directory is set by the $humanndb environment variable
### in the waldronlab/curatedmetagenomics docker container this is:
### /usr/local/humann_datbases
# humanndb="/usr/local/humanndb"
chocophlandir="$humanndb/chocophlan" # chocophlan database directory (nucleotide-database for humann2, like /databases/chocophlan
unirefdir="$humanndb/uniref" # uniref database directory (protein-database for humann2, like /databases/uniref)
mdbn="mpa_v30_CHOCOPhlAn_201901" #metaphlan2 database (like /usr/local/miniconda3/lib/python3.7/site-packages/metaphlan/metaphlan_databases/mpa/v296/CHOCOPhlAn_201901.pkl)

## figure these out by doing `humann3_databases`
urlprefix="http://huttenhower.sph.harvard.edu/humann2_data"

unirefname="uniref90_annotated_v201901.tar.gz"
DEMO_unirefname="uniref90_DEMO_diamond_v201901.tar.gz"
unirefurl="${urlprefix}/uniprot/uniref_annotated/${unirefname}"
DEMO_unirefurl="${urlprefix}/uniprot/uniref_annotated/${DEMO_unirefname}"
#unirefurl="https://www.dropbox.com/s/yeur7nm7ej7spga/uniref90_annotated_v201901.tar.gz?dl=0"

chocophlanname="full_chocophlan.v296_201901.tar.gz"
DEMO_chocophlanname="DEMO_chocophlan.v296_201901.tar.gz"
chocophlanurl="${urlprefix}/chocophlan/${chocophlanname}"
DEMO_chocophlanurl="${urlprefix}/chocophlan/${DEMO_chocophlanname}"
#chocophlanurl="https://www.dropbox.com/s/das8hdof0zyuyh8/full_chocophlan.v296_201901.tar.gz?dl=0"

ncores=2 #number of cores

mkdir -p $chocophlandir
mkdir -p $unirefdir

## For testing purposes, use the reduced ChocoPhlAn and UniRef90 DEMO databases
## A small fastq will be downloaded and profiled
if [ ${run_demo} == 'DEMO' ]; then
    unirefname=${DEMO_unirefname}
    unirefurl=${DEMO_unirefurl}

    chocophlanname=${DEMO_chocophlanname}
    chocophlanurl=${DEMO_chocophlanurl}
fi

if [ ! "$(ls -A $unirefdir)" ]; then
    wget $unirefurl
    tar -xvz -C $unirefdir -f $unirefname
    rm $unirefname
fi

if [ ! "$(ls -A $chocophlandir)" ]; then
    wget $chocophlanurl
    tar -xvz -C $chocophlandir -f $chocophlanname
    rm $chocophlanname
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
if [ ${sample} == 'DEMO' ]; then
    cat $hnn_dir/tests/data/demo.fastq > reads/${sample}.fastq
else
    cat reads/*.fastq > reads/${sample}.fastq
fi

mkdir -p humann
echo 'Running humann'
humann --input reads/${sample}.fastq --output humann --nucleotide-database ${chocophlandir} --protein-database ${unirefdir} --threads=${ncores}
echo 'renorm_table runs'
humann_renorm_table --input humann/${sample}_genefamilies.tsv --output humann/${sample}_genefamilies_relab.tsv --units relab
humann_renorm_table --input humann/${sample}_pathabundance.tsv --output humann/${sample}_pathabundance_relab.tsv --units relab
echo 'run_markers2.py'
run_markers2.py \
    --input_dir humann/${sample}_humann_temp/ \
    --metaphlan_db ${mdbn} \
    --output_dir humann \
    --nprocs ${ncores}

mkdir genefamilies; mv humann/${sample}_genefamilies.tsv genefamilies/${sample}.tsv;
mkdir genefamilies_relab; mv humann/${sample}_genefamilies_relab.tsv genefamilies_relab/${sample}.tsv;
mkdir marker_abundance; mv humann/${sample}.marker_ab_table marker_abundance/${sample}.tsv;
mkdir marker_presence; mv humann/${sample}.marker_pres_table marker_presence/${sample}.tsv;
mkdir metaphlan_bugs_list; mv humann/${sample}_humann_temp/${sample}_metaphlan_bugs_list.tsv metaphlan_bugs_list/${sample}.tsv;
mkdir pathabundance; mv humann/${sample}_pathabundance.tsv pathabundance/${sample}.tsv;
mkdir pathabundance_relab; mv humann/${sample}_pathabundance_relab.tsv pathabundance_relab/${sample}.tsv;
mkdir pathcoverage; mv humann/${sample}_pathcoverage.tsv pathcoverage/${sample}.tsv;
mkdir humann_temp; mv humann/${sample}_humann_temp/ humann_temp/ #comment this line if you don't want to keep humann temporary files

rm -r reads
