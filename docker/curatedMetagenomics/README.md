## Dockerhub

https://hub.docker.com/repository/docker/waldronlab/curatedmetagenomics

## Usage

```
docker run -v /PATH_TO_WHERE_YOU_WANT_OUTPUT:/RUN_PATH_IN_CONTAINER -ti waldronlab/curatedmetagenomics curatedMetagenomicData_pipeline.sh SAMPLENAME SRA_ACCESSION
# a runnable example, where big databases are stored on the host in `${HOME}/biobakery.db`, output goes to `/tmp/output`, and a small demo is run.
export DB_PATH="${HOME}/biobakery.db"; docker run -ti -e ncores=2 -e OUTPUT_PATH=/tmp/containeroutput -v "/tmp/output:/tmp/containeroutput" -v ${DB_PATH}/metaphlan:/usr/local/miniconda3/lib/python3.7/site-packages/metaphlan/metaphlan_databases -v ${DB_PATH}/humann:/usr/local/humann_databases waldronlab/curatedmetagenomics curatedMetagenomicData_pipeline.sh TEST_SAMPLE ERR262957 DEMO
```

### on google genomics api

```
RUN=ERR262957 SAMPLE=TEST_SAMPLE dsub \
--project isb-cgc-04-0020 \
--zones "us-*" \
--logging gs://isb-cgc-04-0020-cromwell-workflows/logs-for-metagenomics \
--env SAMPLE=${SAMPLE} \
--env RUN=${RUN} \
--env ncores=8 \
--output-recursive OUTPUT_PATH=gs://isb-cgc-04-0020-cromwell-workflows/out-for-metagenomics/${SAMPLE}/ \
--image waldronlab/curatedmetagenomics --command 'curatedMetagenomicData_pipeline.sh ${SAMPLE} ${RUN}' \
--min-cores 8 --min-ram 16
```

## Build

```sh
docker build --tag waldronlab/curatedmetagenomics .
```

## Databases

Currently, the `curagedMetagenomicData_pipeline.sh` script alternative publicly accessible databases for uniref and chocophlan, because downloads using `humann3_download` were too slow and unreliable. TODO: create separate scripts for downloading database from Dropbox or Google:

```
unirefname="uniref90_annotated_v201901.tar.gz"
unirefurl="https://www.dropbox.com/s/yeur7nm7ej7spga/uniref90_annotated_v201901.tar.gz?dl=0"

chocophlanname="full_chocophlan.v296_201901.tar.gz"
chocophlanurl="https://www.dropbox.com/s/das8hdof0zyuyh8/full_chocophlan.v296_201901.tar.gz?dl=0"

chocophlandir="$humanndb/chocophlan" # $humanndb is defined within Docker container
unirefdir="$humanndb/uniref"

if [ ! "$(ls -A $unirefdir)" ]; then
    wget $unirefurl
    tar -xvz -C $unirefdir -f $unirefname
    rm $unirefname
fi

if [ ! "$(ls -A $chocophlandir)" ]; then
    wget $chocophlanurl
    tar -xvz -C $chocophlandir -f $chocophlanname
    rm $chocophlanname
fi
```
