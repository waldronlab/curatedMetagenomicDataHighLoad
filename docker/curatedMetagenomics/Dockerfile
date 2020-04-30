FROM ubuntu

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y python3
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get install -y wget

## Install conda
RUN curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN sh Miniconda3-latest-Linux-x86_64.sh -b -p /usr/local/miniconda3
ENV PATH=/usr/local/miniconda3/bin:$PATH
RUN conda config --add channels defaults
RUN conda config --add channels bioconda
RUN conda config --add channels conda-forge

## install metaphlan3 and humann3
RUN conda update conda
RUN conda install -c bioconda metaphlan=3 
RUN conda install -c biobakery humann 

## install sratoolkit
RUN mkdir /tmp/sra
WORKDIR /tmp/sra

RUN curl -O https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.10.5/setup-apt.sh
RUN /bin/bash setup-apt.sh
ENV PATH=/usr/local/ncbi/sra-tools/bin:$PATH

## pipeline run function
COPY curatedMetagenomicData_pipeline.sh download_metaphlandb.sh download_chocophlan.sh download_uniref.sh run_markers2.py /usr/local/bin/
RUN chmod a+rx /usr/local/bin/*.sh /usr/local/bin/run_markers2.py

## interactive user settings workaround
COPY usersettings /root/.ncbi/user-settings.mkfg

RUN rm -rf /tmp/sra /tmp/humann

## display versions
RUN fastq-dump --version
RUN metaphlan --version
RUN humann --version

## root directory for databases
ENV mpa_dir=/usr/local/miniconda3/lib/python3.7/site-packages/metaphlan
ENV hnn_dir=/usr/local/miniconda3/lib/python3.7/site-packages/humann
ENV metaphlandb="${mpa_dir}/metaphlan_databases"
ENV humanndb=/usr/local/humann_databases
ENV chocophlandir="${humanndb}/chocophlan"
ENV unirefdir="${humanndb}/uniref"
RUN mkdir $metaphlandb $humanndb

WORKDIR /root
