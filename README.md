# Overview

Here is a high-level [slide deck](https://www.dropbox.com/s/tawgf4l49190m4o/2020-05-20%20intro%20to%20NCI%201U01%20CA230551%20.pptx?dl=0)

# Major things done

Built a MetaPhlan3 + HUMAnN3 + StrainPhlAn + sratoolkit Docker image.  (see [docker directory](https://github.com/waldronlab/curatedMetagenomicDataHighLoad/tree/master/docker/curatedMetagenomics) for Dockerfile and link to Dockerhub). Instructions to run are kept in a [wiki](https://github.com/waldronlab/curatedMetagenomicDataHighLoad/wiki/Environment-variables-and-invocation). 

There is also a sratoolkit-only docker image (see [docker directory](https://github.com/waldronlab/curatedMetagenomicDataHighLoad/tree/master/docker/sratoolkit), but this is also included in the above all-in-one image. 

# TODO

1. Make a nextflow command for using sratoolkit to download and concatenate fastq
files for given identifiers.  These steps are all performed in `/usr/local/bin/curatedMetagenomicData_pipeline.sh` in the Docker container, which individually calls the steps below. These are within-container commands, see the [wiki](https://github.com/waldronlab/curatedMetagenomicDataHighLoad/wiki/Environment-variables-and-invocation) for full setup and host commands.

```
curatedMetagenomicData_pipeline.sh MV_FEI1_t1Q14 "SRR4052021"
curatedMetagenomicData_pipeline.sh M1.1.SA "SRR2244401;SRR2236793;SRR2243639;SRR2243812;SRR2244215;SRR2245587;SRR2228273;SRR2228283;SRR2228304;SRR2228308;SRR2228313;SRR2228320;SRR2228347;SRR2228399;SRR2226903;SRR2226948;SRR2227815;SRR2228028;SRR2228363;SRR2228450;SRR2228455;SRR2228709"
```

2. Make a nextflow command for running MetaPhlAn3 using the above docker container. 
    - inputs: corresponds to MetaPhlAn3 flags, including fastq input file
    - outputs: three MetaPhlAn output files (bugs list, marker presence, marker abundance)

3. Make a nextflow command for running HUMAnN3:
    - inputs: will be the MetaPhlAn output files
    - outputs: three HUMAnN outputs

4. Create a nextflow command for running StrainPhlAn
    - inputs: will be the MetaPhlAn output files
    - outputs: Not sure what StrainPhlAn outputs are
