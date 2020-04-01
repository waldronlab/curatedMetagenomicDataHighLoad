#!/bin/bash

###note this is currently downloading the DEMO version of the databases!

# databases will go to the S3 location s3://curatedmetagenomics.bioconductor.org/humann2_database_downloads_$humann2_version

source configrc
pip install humann2==$humann2_version

mkdir databases

humann2_databases --download chocophlan DEMO databases/humann2_database_downloads_$humann2_version #DEMO
# humann2_databases --download chocophlan full databases/humann2_database_downloads_$humann2_version #FULL

humann2_databases --download uniref DEMO_diamond databases/humann2_database_downloads_$humann2_version #DEMO
# humann2_databases --download uniref uniref90_diamond databases/humann2_database_downloads_$humann2_version #FULL

aws s3 rm --recursive s3://curatedmetagenomics.bioconductor.org/humann2_database_downloads_$humann2_version
aws s3 cp --recursive databases s3://curatedmetagenomics.bioconductor.org/
