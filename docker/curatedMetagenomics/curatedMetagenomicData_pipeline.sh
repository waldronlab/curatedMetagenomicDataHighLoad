#!/bin/bash

### usage: bash curatedMetagenomicData_pipeline.sh sample_name "SRRxxyxyxx;SRRyyxxyyx"

### before running this script, be sure that these tools are in your path
# fastq-dump
# humann2
# metaphlan
# python

sample=$1
runs=$2

### before running this script, set these paths and variables
pc=/dbs/humann/chocophlan # chocophlan database (nucleotide-database for humann, like /databases/chocophlan
pp=/dbs/humann/uniref # uniref database (protein-database for humann, like /databases/uniref)
pmdb=/opt/metaphlan2/biobakery-metaphlan2/db_v30_CHOCOPhlAn_201901/mpa_v30_CHOCOPhlAn_201901.pkl #metaphlan2 database (like /tools/metaphlan2/db_v20/mpa_v20_m200.pkl)
ncores=2 #number of cores

mkdir -p $pc
mkdir -p $pp

if [ ! "$(ls -A $pp)" ]; then
    wget https://storage.googleapis.com/curatedmetagenomicdata/dbs/uniref/uniref90_annotated_1_1.tar.gz
    tar -xvz -C /dbs/humann/uniref/ -f uniref90_annotated_1_1.tar.gz
fi

if [ ! "$(ls -A $pc)" ]; then
    wget https://storage.googleapis.com/curatedmetagenomicdata/dbs/chocophlan/full_chocophlan_plus_viral.v0.1.1.tar.gz  
    tar -xvz -C /dbs/humann/chocophlan/ -f full_chocophlan_plus_viral.v0.1.1.tar.gz
fi



echo "Working in ${OUTPUT_PATH}"
mkdir -p ${OUTPUT_PATH}

cd ${OUTPUT_PATH}

# while [ "$runs" ] ; do
# 	iter=${runs%%;*}
#         shortyone=$(echo "$iter" | cut -c1-3)
#         shortytwo=$(echo "$iter" | cut -c1-6)
# 	echo 'Starting downloading run '${iter}
#         ${pa}bin/ascp -T -i ${pa}etc/asperaweb_id_dsa.openssh anonftp@ftp.ncbi.nlm.nih.gov:/sra/sra-instant/reads/ByRun/sra/${shortyone}/${shortytwo}/${iter}/${iter}.sra ${sample}/reads/
# 	echo 'Dumping run '${iter}
#         fastq-dump --split-files ${sample}/reads/${iter}.sra --outdir ${sample}/reads/
#         [ "$runs" = "$iter" ] && \
#         runs='' || \
#         runs="${runs#*;}"
# 	echo 'Finished downloading of run '${iter}
# done
fastq-dump --outdir reads $2
echo 'Downloaded.'
echo 'Concatenating runs...'
cat reads/*.fastq > reads/${sample}.fastq

mkdir -p humann
echo 'Running humann'
humann --input reads/${sample}.fastq --output humann --nucleotide-database ${pc} --protein-database ${pp} --threads=${ncores}
echo 'renorm_table runs'
humann_renorm_table --input humann/${sample}_genefamilies.tsv --output humann/${sample}_genefamilies_relab.tsv --units relab
humann_renorm_table --input humann/${sample}_pathabundance.tsv --output humann/${sample}_pathabundance_relab.tsv --units relab
echo 'run_markers2.py'
# NOTE: using absolute path here!!!
python /root/run_markers2.py \
    --input_dir humann/${sample}_humann_temp/ \
    --bt2_ext _metaphlan_bowtie2.txt \
    --metaphlan_db ${pmdb} \
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
mkdir humann_temp; mv humann/${sample}_humann_temp/ humann_temp/ #comment this line if you don't want to keep humann2 temporary files

rm -r reads
