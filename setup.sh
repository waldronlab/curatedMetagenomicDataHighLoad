#!/bin/bash

### usage: bash setup.sh
### Download and build databaeses for humann2 metaphlan2 and bowtie2

##HUMANnN2 Databases ( database : build = location )
##chocophlan : DEMO = http://huttenhower.sph.harvard.edu/humann2_data/chocophlan/DEMO_chocophlan.tar.gz
##chocophlan : full = http://huttenhower.sph.harvard.edu/humann2_data/chocophlan/full_chocophlan.tar.gz
##uniref : DEMO_diamond = http://huttenhower.sph.harvard.edu/humann2_data/uniprot/uniref50_GO_filtered/uniref50_DEMO_diamond.tar.gz
##uniref : diamond = http://huttenhower.sph.harvard.edu/humann2_data/uniprot/uniref50_GO_filtered/uniref50_GO_filtered_diamond.tar.gz
##uniref : rapsearch2 = http://huttenhower.sph.harvard.edu/humann2_data/uniprot/uniref50_GO_filtered/uniref50_GO_filtered_rapsearch2.tar.gz



### HUMANN2 Download Databases
mkdir -p /databases/chocophlan/
cd /databases/chocophlan/
humann2_databases --download chocophlan DEMO humann2_database_downloads
#humann2_databases --download chocophlan full humann2_database_downloads

mkdir -p /databases/uniref/
cd /databases/uniref/
humann2_databases --download uniref DEMO_diamond humann2_database_downloads
#humann2_databases --download uniref diamond humann2_database_downloads

### Metaphlan2 databases download and build
mkdir -p /tools/metaphlan2/db_v20
cd /tools/metaphlan2/db_v20
wget https://bitbucket.org/biobakery/metaphlan2/downloads/mpa_v20_m200.tar
tar xvf mpa_v20_m200.tar
bzip2 -d mpa_v20_m200.fna.bz2
bowtie2-build mpa_v20_m200.fna mpa_v20_m200

