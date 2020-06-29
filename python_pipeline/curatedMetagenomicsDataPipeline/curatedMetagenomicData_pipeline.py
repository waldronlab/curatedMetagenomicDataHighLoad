#!/usr/bin/env python3
import os
import click
import glob
import sys
import subprocess as sb
import shutil
from .utils import make_folder, download_file, download_all, decompress_tar, run_metaphlan, run_humann, run_strainphlan

__author__ = 'Francesco Beghini (francesco.beghini@unitn.it)'
__date__ = 'May 26 2020'
__version__ = '0.0.2'

@click.command()
@click.version_option(version=__version__)
@click.argument('sample_name')
@click.argument('runs')
@click.option('--ncores', envvar='ncores', default="2")
@click.option('--demo', is_flag=True)
@click.argument('output_path')
@click.argument('db_path', required=False)
def pipeline(sample_name, runs, ncores, db_path, output_path, demo):
    """
        Dump from SRA the colon-separated list of RUNS into a FASTQ file named after
        SAMPLE_NAME and profile it with MetaPhlAn, StrainPhlAn, and HUMAnN
    """

    runs = runs.split(';')
    ncores = int(ncores)
    output_path = os.environ.get('OUTPUT_PATH', os.path.dirname(__file__))
    output_path = os.path.expandvars(output_path)
    sys.stdout.write('Output folder is ' + output_path + '\n')

    hnn_dir =  os.path.expandvars(os.environ.get('hnn_dir'))
    if hnn_dir is None:
        sys.exit('hnn_dir env environment variable must be set. Exiting.\n')

    if db_path is None and not demo:
        sys.stdout.write('db_path variable is not set, a clean run will be performed.\nDownloading all the databases...\n')
        db_path = os.getcwd()
        chocophlanname = os.path.expandvars(os.getenv('chocophlanname'))
        chocophlanurl = os.path.expandvars(os.getenv('chocophlanurl'))
        unirefname = os.path.expandvars(os.getenv('unirefname'))
        unirefurl = os.path.expandvars(os.getenv('unirefurl'))
        download_all(db_path, chocophlanname, chocophlanurl, unirefname, unirefurl)
        sys.stdout.write('Done.\n')

    if demo and db_path:
        sample_name = 'DEMO'
        click.echo('Downloading DEMO databases')
        DEMO_unirefname="uniref90_DEMO_diamond_v201901.tar.gz"
        DEMO_unirefurl="https://www.dropbox.com/s/xaisk05u4l822pl/uniref90_DEMO_diamond_v201901.tar.gz?dl=1"
        DEMO_chocophlanname="DEMO_chocophlan.v296_201901.tar.gz"
        DEMO_chocophlanurl="https://www.dropbox.com/s/66wgnzw0eo1z142/DEMO_chocophlan.v296_201901.tar.gz?dl=1"

        download_file(DEMO_unirefurl, DEMO_unirefname)
        decompress_tar(DEMO_unirefname, os.path.expandvars(os.path.join(db_path, 'humann', 'uniref')))
        os.unlink(DEMO_unirefname)

        download_file(DEMO_chocophlanurl, DEMO_chocophlanname)
        decompress_tar(DEMO_chocophlanname, os.path.expandvars(os.path.join(db_path, 'humann', 'chocophlan')))
        os.unlink(DEMO_chocophlanname)
    else:
        sys.stdout.write('db_path variable must be set. Exiting.\n')

    try:
        sb.check_call(['fasterq-dump', '-h'], stderr=sb.DEVNULL, stdout=sb.DEVNULL)
    except:
        sys.exit('fasterq-dump is not present in the system path. Exiting.\n')

    make_folder(os.path.join(output_path,'reads'))
           
    for run in runs:
        sys.stdout.write('Dumping run {}\n'.format(run))
        sb.check_call([ 'fasterq-dump', 
                        '-t', output_path, 
                        '--force', 
                        '--threads', str(ncores), 
                        '--split-files', run, 
                        '--outdir', os.path.join(output_path,'reads')
                    ])
        sys.stdout.write('Finished downloading of run {}\n'.format(run))

    sys.stdout.write('Downloaded all runs.\n')
    sys.stdout.write('Concatenating runs...\n')

    with open(os.path.join(output_path, 'reads', '{}.fastq'.format(sample_name)), 'w') as sample_file:
        if demo:
            with open('{}/tests/data/demo.fastq'.format(hnn_dir)) as demo_fasta:
                shutil.copyfileobj(demo_fasta, sample_file)
        else:
            for fq_path in glob.glob(os.path.join(output_path, 'reads', '*.fastq')):
                with open(fq_path) as fq_file:
                    shutil.copyfileobj(fq_file, sample_file)

    if os.path.isfile(os.path.join(output_path, 'reads', '{}.fastq'.format(sample_name))):
        click.echo('Running metaphlan')
        run_metaphlan(sample_name, db_path, output_path, ncores)
    else:
        sys.exit('MetaPhlAn execution has failed. Cannot find the input metagenome. Exiting.')

    if os.path.isfile(os.path.join(output_path, 'metaphlan', '{}.sam.bz2'.format(sample_name))):
        click.echo('Running strainphlan')
        run_strainphlan(sample_name, output_path, ncores)
    else:
        sys.exit('MetaPhlAn execution has failed, the output SAM file is missing. StrainPhlAn can not be executed. Exiting.')

    if os.path.isfile(os.path.join(output_path, 'metaphlan_bugs_list', '{}.tsv'.format(sample_name))):
        click.echo('Running humann')
        run_humann(sample_name, db_path, output_path, ncores)
    else:
        sys.exit('MetaPhlAn execution has failed, the output profile file is missing. HUMAnN can not be executed. Exiting.')

    for f in ['humann', 'reads']:
        shutil.rmtree(os.path.join(output_path, f))
