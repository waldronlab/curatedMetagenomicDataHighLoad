#!/usr/bin/env python3
import os
import glob
import sys
import argparse as ap
import subprocess as sb
from urllib.request import urlretrieve
import tarfile

__author__ = 'Francesco Beghini (francesco.beghini@unitn.it)'
__date__ = 'May 26 2020'

def read_params():
    p = ap.ArgumentParser(description="")
    p.add_argument( '--sample_name', 
                    type=str, 
                    required=True,
                    help="Name of the sample")
    p.add_argument( '--runs', 
                    type=str, 
                    required=True,
                    help="Colon-separated list of SRR ids")
    p.add_argument( '--demo', 
                    action="store_true"
                    help="If set, a DEMO sample will be profiled")
    return p.parse_args()

def make_folder(path):
    if not os.path.isdir(path):
        try:
            os.makedirs(path)
        except EnvironmentError:
            sys.exit("ERROR: Unable to create folder {}".format(path))

def download(url, file_path):
    try:
        sys.stderr.write("\nDownloading " + url + "\n")
        file, headers = urlretrieve(url, file_path)
    except EnvironmentError:
        sys.stderr.write("\nWarning: Unable to download " + url + "\n")

def decompress_tar(tar_file, destination):
    try:
        tarfile_handle = tarfile.open(tar_file)
        tarfile_handle.extractall(path=destination)
        tarfile_handle.close()
    except EnvironmentError:
        sys.stderr.write("Warning: Unable to extract {}.\n".format(tar_file))

if __name__ == '__main__':
    args = read_params()

    sample_name = args.sample
    runs = args.runs.split(';')

    ncores = os.environ.get('ncores', 2)
    output_path = os.environ.get('OUTPUT_PATH', os.path.abspath(__file__))
    
    hnn_dir = os.environ.get('hnn_dir')
    if hnn_dir is None:
        sys.exit('hnn_dir env environment variable must be set. Exiting.\n')

    metaphlandb = os.environ.get('metaphlandb')
    if metaphlandb is None:
        sys.exit('metaphlandb env environment variable must be set. Exiting.\n')

    humanndb = os.environ.get('humanndb')
    if humanndb is None:
        sys.exit('humanndb env environment variable must be set. Exiting.\n')
        
    chocophlandir = os.environ.get('chocophlandir')
    if chocophlandir is None:
        sys.exit('chocophlandir env environment variable must be set. Exiting.\n')
    else:
        make_folder(chocophlandir)

    unirefdir = os.environ.get('unirefdir')
    if unirefdir is None:
        sys.exit('unirefdir env environment variable must be set. Exiting.')
    else:
        make_folder(unirefdir)

    if args.demo:
        DEMO_unirefname="uniref90_DEMO_diamond_v201901.tar.gz"
        DEMO_unirefurl="https://www.dropbox.com/s/xaisk05u4l822pl/uniref90_DEMO_diamond_v201901.tar.gz?dl=1"
        DEMO_chocophlanname="DEMO_chocophlan.v296_201901.tar.gz"
        DEMO_chocophlanurl="https://www.dropbox.com/s/66wgnzw0eo1z142/DEMO_chocophlan.v296_201901.tar.gz?dl=1"

        download(DEMO_unirefurl, DEMO_unirefname)
        decompress_tar(DEMO_unirefname, unirefdir)
        os.unlink(DEMO_unirefname)

        download(DEMO_chocophlanurl, DEMO_chocophlanname)
        decompress_tar(DEMO_chocophlanname, chocophlandir)
        os.unlink(DEMO_chocophlanname)
    try:
        sb.check_call(['fasterq-dump', '-h'], stderr=sb.DEVNULL, stdout=sb.DEVNULL)
    except:
        sys.exit('fasterq-dump is not present in the system path. Exiting.\n')

    make_folder('reads')
           
    for run in runs:
        sys.stdout.write('Dumping run {}\n'.format(run))
        sb.check_call(['fasterq-dump', '--threads', ncores, '--split-files', run, '--outdir', 'reads'], stderr=sb.DEVNULL, stdout=sb.DEVNULL)
        sys.stdout.write('Finished downloading of run {}\n'.format(run))

    sys.stdout.write('Downloaded all runs.\n')
    sys.stdout.write('Concatenating runs...\n')

    with open(os.path.join('reads', '{}.fastq'.format(sample_name)), 'w') as sample_file:
        if args.demo:
            with open('{}/tests/data/demo.fastq'.format(hnn_dir)) as demo_fasta:
                shutil.copyfileobj(demo_fasta, sample_file)
        else:
            for fq_path in glob.glob('reads/*.fastq'):
                with open(fq_path) as fq_file:
                    shutil.copyfileobj(fq_file, sample_file)

    make_folder('metaphlan')