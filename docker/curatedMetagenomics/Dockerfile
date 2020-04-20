FROM bioconda/bioconda-utils-build-env

RUN conda update conda
RUN conda install -c bioconda metaphlan=3
RUN conda create -n humann-3alpha metaphlan=3
RUN git clone https://github.com/biobakery/humann.git
RUN pwd
WORKDIR humann
RUN pwd
RUN ls -alt
RUN git checkout 3.0.0-alpha
RUN python setup.py install

## SRA Toolkit
RUN conda install -c bioconda sra-tools

## pipeline run function
WORKDIR /root
COPY curatedMetagenomicData_pipeline.sh /root/
RUN chmod a+rwx /root/curatedMetagenomicData_pipeline.sh

## display versions
# RUN fastqdump --version
RUN metaphlan --version
RUN humann3 --version

WORKDIR /root
