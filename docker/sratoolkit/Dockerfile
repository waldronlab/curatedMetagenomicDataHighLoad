FROM ubuntu

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y python3
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get install -y wget

## install sratoolkit
RUN mkdir /tmp/sra
WORKDIR /tmp/sra

RUN curl -O https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.10.5/setup-apt.sh
RUN /bin/bash setup-apt.sh
ENV PATH=/usr/local/ncbi/sra-tools/bin:$PATH

## interactive user settings workaround
COPY usersettings /root/.ncbi/user-settings.mkfg

RUN rm -rf /tmp/sra

WORKDIR /root