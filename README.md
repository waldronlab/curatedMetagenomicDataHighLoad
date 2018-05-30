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
  ```
  #sudo apt-get install -y docker.io #install Docker if needed
  docker pull stevetsa/curatedmetagenomicdatahighload
  docker run -it stevetsa/curatedmetagenomicdatahighload
  ## mount the current directory in the container for debugging
  #docker run -v `pwd`:`pwd` -w `pwd` -i -t stevetsa/curatedmetagenomicdatahighload
  ## once in container, set up databases (line 19-40 in [script](https://github.com/stevetsa/curatedMetagenomicDataHighLoad/blob/master/curatedMetagenomicData_pipeline.sh)) then run
  bash curatedMetagenomicData_pipeline.sh MV_FEI4_t1Q14 "SRR4052038"
  ```
