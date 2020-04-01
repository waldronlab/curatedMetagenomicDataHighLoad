The scripts in the sean_nextflow directory allow the user to reproduce
the entire process of downloading raw reads, process them with the
MetaPhlAn2 and HUMAnN2 pipelines, generate the final normalized
profiles, and arrange them in folders exactly as done for the package.

Levi temporarily moved everything there to allow a fresh start in the
main directory, copying things back here as needed. Some things that
need to be done:

1. Build a MetaPhlan3 Docker image using
Bioconda to install. The Bioconda install command for MetaPhlAn3 is:
```
conda install -c bioconda metaphlan=3
```

Maybe based on https://hub.docker.com/r/conda/miniconda3? Will have to
test.

2. Build a sratoolkit docker image (see docker directory for Dockerfile)

3. Make a nextflow command for using sratoolkit to download and concatenate fastq
files for given identifiers.  See
`pipelines/curatedMetagenomicData_pipeline.sh` for sratoolkit
code (up until the line `cat ${sample}/reads/*.fastq > ${sample}/reads/${sample}.fastq`).
Here are two examples for testing that demonstrate one sample coming from a
single fastq file and another coming from many. 

```
bash curatedMetagenomicData_pipeline.sh MV_FEI1_t1Q14 "SRR4052021"
bash curatedMetagenomicData_pipeline.sh M1.1.SA "SRR2244401;SRR2236793;SRR2243639;SRR2243812;SRR2244215;SRR2245587;SRR2228273;SRR2228283;SRR2228304;SRR2228308;SRR2228313;SRR2228320;SRR2228347;SRR2228399;SRR2226903;SRR2226948;SRR2227815;SRR2228028;SRR2228363;SRR2228450;SRR2228455;SRR2228709"
```


4. Make a nextflow command for running MetaPhlAn3 using the above docker container. 
    - inputs: corresponds to MetaPhlAn3 flags, including fastq input file
    - outputs: three MetaPhlAn output files (bugs list, marker presence, marker abundance)

5. Add HUMAnN3 + StrainPhlAn to the above container

6. Make a nextflow command for running HUMAnN3:
    - inputs: will be the MetaPhlAn output files
    - outputs: three HUMAnN outputs

7. Create a nextflow command for running StrainPhlAn
    - inputs: will be the MetaPhlAn output files
    - outputs: Not sure what StrainPhlAn outputs are


# Notes about what is here

* A single sample can be downloaded and processed as follows:

   ```$ bash curatedMetagenomicData_pipeline.sh sample_name "SRRxxyxyxx;SRRyyxxyyx"``` 

   where `sample_name` is the name to be given to the sample, and SRRxxyxyxx etc are the relative NCBI accession numbers.

   See within `curatedMetagenomicData_pipeline.sh` for requirements and settings.

* `sample_name` and relative NCBI accession numbers for all the samples included in the package are available in the 'combined_metadata' dataset provided in the package:

   ```
   > library(curatedMetagenomicData)
   > data(combined_metadata)
   ```

* All the samples included in the package can be downloaded and processed by running the commands in

   `curatedMetagenomicData_pipeline_allsamples.sh`

   Please be aware that this would take ages to be run on a single CPU.

* Follow the same procedure if you want to process your own dataset.

* When done, your output profile files are properly organized and ready to be [included](https://github.com/waldronlab/curatedMetagenomicData/wiki/The-curatedMetagenomicData-pipelines) in the *curatedMetagenomicData* package.

* To run the [Docker container](https://hub.docker.com/r/stevetsa/curatedmetagenomicdatahighload/)  
  This container is automatically build from the Dockerfile in [GitHub](https://github.com/stevetsa/curatedMetagenomicDataHighLoad)  
  There are some [confusion](https://groups.google.com/forum/#!topic/metaphlan-users/t6IV1PxgNNA) about the location of the databases for the new Metaphlan2.
  The get-around is to duplicate the database files for metaphlan in two locations metaphlan2/db_v20 and metaphlan2/databases/  
  On AWS m5.4xlarge instance, with 50GB Volume attached.  "SRR4052038" below took about 30 min.   

  ```
  #sudo apt-get install -y docker.io #install Docker if needed
  docker pull stevetsa/curatedmetagenomicdatahighload
  docker run -it stevetsa/curatedmetagenomicdatahighload

  ## mount the current directory in the container for debugging
  #docker run -v `pwd`:`pwd` -w `pwd` -i -t stevetsa/curatedmetagenomicdatahighload

  ## Inside container - 
  git clone https://github.com/stevetsa/curatedMetagenomicDataHighLoad.git
  cd curatedMetagenomicDataHighLoad
  bash setup.sh
  bash curatedMetagenomicData_pipeline.sh MV_FEI4_t1Q14 "SRR4052038" 
  ```

# New components for dockerization

* `configrc`: source this to set version numbers or other configurations
* `download_humann2_databases.sh`: Install humann2, download its uniref and chocophlan databases, and copy these to *s3://curatedmetagenomics.bioconductor.org/humann2_database_downloads_$humann2_version*. Note this also requires environment variables *AWS_SECRET_ACCESS_KEY* and *AWS_ACCESS_KEY_ID* to be set
* `parsemetadata.sh`: specify a `_metadata.tsv` filename and return pipeline commands in the format of `curatedMetagenomicData_pipeline_allsamples.sh` to *stdout*.
