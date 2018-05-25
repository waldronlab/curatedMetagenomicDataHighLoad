FROM ubuntu:16.04
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
MAINTAINER Steve Tsang <mylagimail2004@yahoo.com>

RUN apt-get update && apt-get install --yes \
 build-essential \
 gcc-multilib \
 apt-utils \
 zlib1g-dev \
 wget \
 git \
 python-pip \
 python-dev \
 libbz2-dev \
 liblzma-dev \
 apt-utils \
 libz-dev \
 ncurses-dev \
 zlib1g-dev \
 libxml2-dev \
 python-numpy \
 python-scipy \
 python-matplotlib \
 mercurial \
 perl \
 unzip

RUN mkdir /tools
## install SRA tool kit
WORKDIR /tools
RUN wget https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/current/sratoolkit.current-ubuntu64.tar.gz
RUN tar xvzf sratoolkit.current-ubuntu64.tar.gz
WORKDIR /tools/sratoolkit.2.9.0-ubuntu64
ENV PATH="/tools/sratoolkit.2.9.0-ubuntu64/bin:${PATH}"

## Install HUMANN2 and set up databases
RUN pip install --upgrade pip 
RUN pip install humann2

RUN mkdir -p /databases/chocophlan/
WORKDIR /databases/chocophlan/
RUN humann2_databases --download chocophlan DEMO humann2_database_downloads

RUN mkdir -p /databases/uniref/
WORKDIR /databases/uniref/
RUN humann2_databases --download uniref DEMO_diamond humann2_database_downloads

## Install metaphlan
WORKDIR /tools
RUN hg clone https://bitbucket.org/biobakery/metaphlan2
ENV PATH="/tools/metaphla2:${PATH}"
ENV mpa_dir="/tools/metaphlan2"

## Install BowTie2
WORKDIR /tools
RUN wget https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.3.4.1/bowtie2-2.3.4.1-linux-x86_64.zip
RUN unzip bowtie2-2.3.4.1-linux-x86_64.zip

## Install Aspera
RUN wget https://download.asperasoft.com/download/sw/cli/3.7.7/aspera-cli-3.7.7.608.927cce8-linux-64-release.sh
RUN bash aspera-cli-3.7.7.608.927cce8-linux-64-release.sh
ENV PATH="/root/.aspera/cli/bin:${PATH}"
RUN mkdir -p /tools/aspera/connect/bin/
RUN cp /root/.aspera/cli/bin/* /tools/aspera/connect/bin/.

ENV pa="/root/.aspera/cli/bin"
ENV pm="/tools/metaphlan2/metaphlan2.py"
ENV pc="/databases/chocophlan/"
ENV pp="/databases/uniref/"
ENV pmdb="/tools/metaphlan2/db_v20/mpa_v20_m200.pkl" 
ENV ncores="16"

WORKDIR /
RUN git clone https://github.com/waldronlab/curatedMetagenomicDataHighLoad.git
