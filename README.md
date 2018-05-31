The scripts in this directory allow the user to reproduce the entire process of downloading raw reads, process them with the  MetaPhlAn2 and HUMAnN2 pipelines, generate the final normalized profiles, and arrange them in folders exactly as done for the package.

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
