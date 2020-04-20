FROM bioconda/bioconda-utils-build-env

RUN conda update conda
RUN conda install -c bioconda metaphlan=3
RUN metaphlan --version

## SRA Toolkit
RUN conda install -c bioconda sra-tools
RUN fastqdump --version

WORKDIR /root
