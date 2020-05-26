#!/usr/bin/env python3
import os
import sys
import argparse as ap
from urllib.request import urlretrieve
import tar

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
                    type=str, 
                    required=False,
                    help="If set, a DEMO sample will be profiled")
    return p.parse_args()

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

    ncores = os.environ.get('ncores')
    output_path = os.environ.get('OUTPUT_PATH')
    metaphlandb = os.environ.get('metaphlandb')
    humanndb = os.environ.get('humanndb')
    chocophlandir = os.environ.get('chocophlandir')
    unirefdir = os.environ.get('unirefdir')

    if args.demo is not None:
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