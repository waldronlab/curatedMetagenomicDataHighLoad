FROM bioconda/bioconda-utils-build-env

RUN conda update conda
RUN conda install -c bioconda metaphlan=3

## SRA Toolkit
RUN curl https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/current/sratoolkit.current-centos_linux64.tar.gz > sratoolkit.current-centos_linux64.tar.gz
RUN tar xfz sratoolkit.current-centos_linux64.tar.gz
RUN rm *log sratoolkit.current-centos_linux64.tar.gz
RUN srabin=$PWD/`find . -name "sratoolkit*" -type d`/bin
ENV PATH=$PATH:$srabin

WORKDIR /root

