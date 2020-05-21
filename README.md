# Overview

Here is a high-level [slide deck](https://www.dropbox.com/s/tawgf4l49190m4o/2020-05-20%20intro%20to%20NCI%201U01%20CA230551%20.pptx?dl=0)

See the [wiki](https://github.com/waldronlab/curatedMetagenomicDataHighLoad/wiki/Environment-variables-and-invocation) for full setup and execution instructions.

# Done

Built a MetaPhlan3 + HUMAnN3 + StrainPhlAn + sratoolkit Docker image.  (see [docker directory](https://github.com/waldronlab/curatedMetagenomicDataHighLoad/tree/master/docker/curatedMetagenomics) for Dockerfile and link to Dockerhub). Instructions to run are kept in a [wiki](https://github.com/waldronlab/curatedMetagenomicDataHighLoad/wiki/Environment-variables-and-invocation). There is still work to be done turning bash scripts into a Python package with improved documentation, arguments, and versioning.

There is also a sratoolkit-only docker image (see [docker directory](https://github.com/waldronlab/curatedMetagenomicDataHighLoad/tree/master/docker/sratoolkit), but this is also included in the above all-in-one image. 

# TODO

1. Make a nextflow command for using sratoolkit to download and concatenate fastq
files for given identifiers.  These steps are all performed in `/usr/local/bin/curatedMetagenomicData_pipeline.sh` in the Docker container, which individually calls the steps below. See the [wiki](https://github.com/waldronlab/curatedMetagenomicDataHighLoad/wiki/Environment-variables-and-invocation) for full setup and execution instructions.

2. Make a nextflow command for running MetaPhlAn3 using the above docker container. 
    - inputs: corresponds to MetaPhlAn3 flags, including fastq input file
    - outputs: three MetaPhlAn output files (bugs list, marker presence, marker abundance)

3. Make a nextflow command for running HUMAnN3:
    - inputs: will be the MetaPhlAn output files
    - outputs: three HUMAnN outputs

4. Create a nextflow command for running StrainPhlAn
    - inputs: will be the MetaPhlAn output files
    - outputs: Not sure what StrainPhlAn outputs are
