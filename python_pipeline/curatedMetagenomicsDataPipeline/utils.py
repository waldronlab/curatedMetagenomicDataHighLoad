#!/usr/bin/env python3
import click
import argparse as ap
import os
import sys
import shutil
from urllib.request import urlretrieve
import subprocess as sb
import tarfile

@click.group(help="Command-line suite utilities for curatedMetagenomicsData")
def cli():
    pass

def make_folder(path):
    if not os.path.isdir(path):
        try:
            os.makedirs(path)
        except EnvironmentError:
            sys.exit("ERROR: Unable to create folder {}".format(path))

@cli.group(help="Commands for downloading databases")
def download():
    pass

@download.command('download_file', help='Download a file in a choosen destination')
@click.argument('url')
@click.argument('file_path')
def download_file(url, file_path):
    # try:
    sys.stderr.write("\nDownloading " + url + "\n")
    file, headers = urlretrieve(url, file_path)
    # except EnvironmentError:
        # sys.stderr.write("\nWarning: Unable to download " + url + "\n")

def decompress_tar(tar_file, destination):
    try:
        tarfile_handle = tarfile.open(tar_file)
        tarfile_handle.extractall(path=destination)
        tarfile_handle.close()
    except EnvironmentError:
        sys.stderr.write("Warning: Unable to extract {}.\n".format(tar_file))

@download.command('metaphlan_database', help='Download and install the latest available MetaPhlAn database')
@click.argument('metaphlandb', envvar='metaphlandb', type=click.Path())
def download_metaphlan_databases(metaphlandb):
    sb.check_call(
    ['metaphlan',
    '--install', 
    '--index','latest', 
    '--bowtie2db', metaphlandb
    ])

@download.command('chocophlan', help='Download annotated CHOCOPhlAn pangenomes')
@click.argument('chocophlandir', envvar='chocophlandir')
@click.argument('chocophlanname', envvar='chocophlanname', type=click.File('w'))
@click.argument('chocophlanurl', envvar='chocophlanurl')
def download_chocophlan(chocophlandir, chocophlanname, chocophlanurl):
    make_folder(chocophlandir)
    
    if chocophlanurl.startswith("https://storage.googleapis.com") and shutil.which('gsutil') is not None:
        sb.check_call(['gsutil', 'cp', 'gs://humann2_data/'+ chocophlanname,  '.'])
    else:
        download_file(chocophlanurl, os.path.join(os.path.abspath(__file__), chocophlanname.name))
    decompress_tar(os.path.join(os.path.abspath(__file__), chocophlanname.name), chocophlandir)
    os.unlink(os.path.join(os.path.abspath(__file__), chocophlanname.name))

@download.command('uniref', help='Download UniRef database')
@click.argument('unirefdir', envvar='unirefdir', type=click.Path())
@click.argument('unirefname', envvar='unirefname')
@click.argument('unirefurl', envvar='unirefurl')
def download_uniref(unirefdir, unirefname, unirefurl):
    make_folder(unirefdir)

    if unirefurl.startswith("https://storage.googleapis.com") and shutil.which('gsutil') is not None:
        sb.check_call(['gsutil', 'cp', 'gs://humann2_data/'+ unirefname,  '.'])
    else:
        download_file(unirefurl, os.path.join(os.path.abspath(__file__), unirefname))
    decompress_tar(os.path.join(os.path.abspath(__file__), unirefname), unirefdir)
    os.unlink(os.path.join(os.path.abspath(__file__), unirefname))


@cli.group(help="Commands for running profiling tools")
def run():
    pass

@run.command('metaphlan', help='Run MetaPhlAn on a sample')
@click.argument('sample_name')
@click.argument('metaphlandb', envvar='metaphlandb')
@click.argument('ncores', envvar='ncores', default=2, type=click.INT)
def run_metaphlan(sample_name, metaphlandb, ncores):
    for d in ['metaphlan', 'marker_abundance', 'marker_presence', 'metaphlan_bugs_list']:
        make_folder(d)
    
    sb.check_call(
    ['metaphlan',
    '--input_type', 'fastq','--index', 'latest',
    '--bowtie2db', metaphlandb,
    '--samout', os.path.join('metaphlan', '{}.sam.bz2'.format(sample_name)),
    '--bowtie2out',  os.path.join('metaphlan', '{}.bowtie2out'.format(sample_name)),
    '--nproc', ncores,
    '-o', os.path.join('metaphlan_bugs_list', '{}.tsv'.format(sample_name)),
    os.path.join('reads', '{}.fastq'.format(sample_name))])

    sb.check_call(
    ['metaphlan',
    '--input_type', 'bowtie2out','--index', 'latest',
    '--bowtie2db', metaphlandb,
    '-t', 'marker_pres_table',
    '-o', os.path.join('marker_presence', '{}.tsv'.format(sample_name)),
    os.path.join('metaphlan', '{}.bowtie2out'.format(sample_name))
    ])
    
    sb.check_call(
    ['metaphlan',
    '--input_type', 'bowtie2out', '--index', 'latest',
    '--bowtie2db', metaphlandb,
    '-t', 'marker_ab_table',
    '-o', os.path.join('marker_abundance', '{}.tsv'.format(sample_name)),
    os.path.join('metaphlan', '{}.bowtie2out'.format(sample_name))
    ])

@run.command('strainphlan', help='Run StrainPhlAn on a sample')
@click.argument('sample_name')
@click.argument('ncores', envvar='ncores', default=2, type=click.INT)
def run_strainphlan(sample_name, ncores):
    make_folder('consensus_markers')
    
    sb.check_call([ 'sample2markers.py', 
                    '-i', os.path.join('metaphlan', '{}.sam.bz2'.format(sample_name)),
                    '-o', 'consensus_markers',
                    '-n', ncores]
                )


@run.command('humann', help='Run HUMAnN on a sample')
@click.argument('sample_name')
@click.argument('chocophlandir', envvar='chocophlandir')
@click.argument('unirefdir', envvar='unirefdir')
@click.argument('metaphlandb', envvar='metaphlandb')
@click.argument('ncores', envvar='ncores', default=2, type=click.INT)
def run_humann(sample_name, chocophlandir, unirefdir, metaphlandb, ncores):
    for d in ['humann','genefamilies','genefamilies_relab','genefamilies_cpm','pathabundance','pathabundance_relab','pathcoverage','pathabundance_cpm']:
        make_folder(d)
    
    sb.check_call([ 'humann',
                    '--input', os.path.join('reads', '{}.fastq'.format(sample_name)),
                    '--output', 'humann',
                    '--nucleotide-database', chocophlandir, 
                    '--taxonomic-profile', os.path.join('metaphlan_bugs_list', '{}.tsv'.format(sample_name)),
                    '--protein-database', unirefdir,
                    '--metaphlan-options', '"--bowtie2db {}"'.format(metaphlandb), 
                    '--threads', ncores]
                )

if __name__ == '__main__':
    cli()