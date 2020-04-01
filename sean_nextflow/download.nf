#!/usr/bin/env nextflow

params.humann2_version = "0.11.1"

process download {
    cpus 2
    
    publishDir("s3://curatedmetagenomics.bioconductor.org/databases")
    
    output:
    file('databases/**') into downloaded

    shell:
    humann2_version="${params.humann2_version}"
    """
    pip install humann2==$humann2_version

    mkdir databases

    humann2_databases --download chocophlan DEMO databases/humann2_database_downloads_$humann2_version & #DEMO 
    humann2_databases --download chocophlan full databases/humann2_database_downloads_$humann2_version & #FULL

    humann2_databases --download uniref DEMO_diamond databases/humann2_database_downloads_$humann2_version & #DEMO
    humann2_databases --download uniref uniref90_diamond databases/humann2_database_downloads_$humann2_version & #FULL
    touch databases/.version_${humann2_version}
    wait()
    """
}


abc.subscribe { println ( it ) }