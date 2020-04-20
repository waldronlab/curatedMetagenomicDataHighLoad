FROM ubuntu

WORKDIR /root

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y python3
RUN apt-get install -y curl
RUN apt-get install -y git

## Install conda
RUN curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN sh Miniconda3-latest-Linux-x86_64.sh -b
ENV PATH=/root/miniconda3/bin:$PATH
RUN echo $PATH
RUN conda config --add channels defaults
RUN conda config --add channels bioconda
RUN conda config --add channels conda-forge

## install metaphlan3 and humann3
RUN conda update conda
RUN conda install -c bioconda metaphlan=3
RUN conda create -n humann-3alpha metaphlan=3
RUN git clone https://github.com/biobakery/humann.git
WORKDIR /root/humann
RUN git checkout 3.0.0-alpha
RUN python setup.py install

## install sratoolkit
RUN mkdir /root/tmp
WORKDIR /root/tmp

RUN curl -O https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.10.5/setup-apt.sh
RUN /bin/bash setup-apt.sh
ENV PATH=/usr/local/ncbi/sra-tools/bin:$PATH
RUN echo $PATH

## pipeline run function
WORKDIR /root
COPY curatedMetagenomicData_pipeline.sh /root/
RUN chmod a+rwx /root/curatedMetagenomicData_pipeline.sh

## interactive user settings workaround
COPY usersettings /root/.ncbi/user-settings.mkfg

RUN rm -rf /root/tmp /root/humann

## display versions
RUN fastq-dump --version
RUN metaphlan --version
RUN humann3 --version


WORKDIR /root
