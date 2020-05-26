import argparse as ap
import os
import sys
import shutil
from urllib.request import urlretrieve
import subprocess as sb
import tarfile

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
                    action="store_true",
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


def run_metaphlan(sample, metaphlandb, ncores):
    for d in ['marker_abundance', 'marker_presence', 'metaphlan_bugs_list']:
        make_folder(d)
    
    sb.check_call(
    ['metaphlan',
    '--input_type', 'fastq','--index', 'latest',
    '--bowtie2db', metaphlandb,
    '--samout', os.path.join('metaphlan', '{}.sam.bz2'.format(sample)),
    '--bowtie2out',  os.path.join('metaphlan', '{}.bowtie2out'.format(sample)),
    '--nproc', ncores,
    '-o', os.path.join('metaphlan_bugs_list', '{}.tsv'.format(sample)),
    os.path.join('reads', '{}.fastq'.format(sample))])

    sb.check_call(
    ['metaphlan',
    '--input_type', 'bowtie2out','--index', 'latest',
    '--bowtie2db', metaphlandb,
    '-t', 'marker_pres_table',
    '-o', os.path.join('marker_presence', '{}.tsv'.format(sample)),
    os.path.join('metaphlan', '{}.bowtie2out'.format(sample))
    ])
    
    sb.check_call(
    ['metaphlan',
    '--input_type', 'bowtie2out', '--index', 'latest',
    '--bowtie2db', metaphlandb,
    '-t', 'marker_ab_table',
    '-o', os.path.join('marker_abundance', '{}.tsv'.format(sample)),
    os.path.join('metaphlan', '{}.bowtie2out'.format(sample))
    ])

def run_strainphlan(sample, ncores):
    make_folder('consensus_markers')
    
    sb.check_call([ 'sample2markers.py', 
                    '-i', os.path.join('metaphlan', '{}.sam.bz2'.format(sample)),
                    '-o', 'consensus_markers',
                    '-n', ncores]
                )

def run_humann(sample, chocophlandir, unirefdir, metaphlandb, ncores)