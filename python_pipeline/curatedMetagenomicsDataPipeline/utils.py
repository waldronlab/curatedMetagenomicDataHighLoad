#!/usr/bin/env python3
import click
import argparse as ap
import os
import sys
import shutil
from urllib.request import urlretrieve
import subprocess as sb
import tarfile
import time

def make_folder(path):
    if not os.path.isdir(path):
        try:
            os.makedirs(path)
        except EnvironmentError:
            sys.exit("ERROR: Unable to create folder {}".format(path))

def byte_to_megabyte(byte):
    """
    Convert byte value to megabyte
    """

    return byte / (1024.0**2)

class ReportHook():
    def __init__(self):
        self.start_time = time.time()

    def report(self, blocknum, block_size, total_size):
        """
        Print download progress message
        """

        if blocknum == 0:
            self.start_time = time.time()
            if total_size > 0:
                sys.stderr.write("Downloading file of size: {:.2f} MB\n"
                                 .format(byte_to_megabyte(total_size)))
        else:
            total_downloaded = blocknum * block_size
            status = "{:3.2f} MB ".format(byte_to_megabyte(total_downloaded))

            if total_size > 0:
                percent_downloaded = total_downloaded * 100.0 / total_size
                # use carriage return plus sys.stderr to overwrite stderr
                download_rate = total_downloaded / (time.time() - self.start_time)
                estimated_time = (total_size - total_downloaded) / download_rate
                estimated_minutes = int(estimated_time / 60.0)
                estimated_seconds = estimated_time - estimated_minutes * 60.0
                status += ("{:3.2f} %  {:5.2f} MB/sec {:2.0f} min {:2.0f} sec "
                           .format(percent_downloaded,
                                   byte_to_megabyte(download_rate),
                                   estimated_minutes, estimated_seconds))

            status += "        \r"
            sys.stderr.write(status)

def download_file(url, file_path):
    try:
        sys.stderr.write("\nDownloading " + url + "\n")
        file, headers = urlretrieve(url, file_path, reporthook=ReportHook().report)
    except EnvironmentError:
        sys.stderr.write("\nWarning: Unable to download " + url + "\n")

def decompress_tar(tar_file, destination):
    try:
        tarfile_handle = tarfile.open(tar_file)
        tarfile_handle.extractall(path=destination)
        tarfile_handle.close()
    except EnvironmentError:
        sys.stderr.write("Warning: Unable to extract {}.\n".format(tar_file))

def download_metaphlan_databases(metaphlandb):
    metaphlandb = os.path.expandvars(metaphlandb)
    sb.check_call(
    ['metaphlan',
    '--install', 
    '--index','latest', 
    '--bowtie2db', metaphlandb
    ])

def download_chocophlan(chocophlandir, chocophlanname, chocophlanurl):
    chocophlandir = os.path.expandvars(chocophlandir)
    chocophlanurl = os.path.expandvars(chocophlanurl)
    make_folder(chocophlandir)
    
    if chocophlanurl.startswith("https://storage.googleapis.com") and shutil.which('gsutil') is not None:
        sb.check_call(['gsutil', 'cp', 'gs://humann2_data/'+ chocophlanname,  '.'])
    else:
        download_file(chocophlanurl, os.path.join(chocophlandir, chocophlanname))
    decompress_tar(os.path.join(chocophlandir, chocophlanname), chocophlandir)
    os.unlink(os.path.join(chocophlandir, chocophlanname))

def download_uniref(unirefdir, unirefname, unirefurl):
    unirefdir = os.path.expandvars(unirefdir)
    unirefurl = os.path.expandvars(unirefurl)
    make_folder(unirefdir)

    if unirefurl.startswith("https://storage.googleapis.com") and shutil.which('gsutil') is not None:
        sb.check_call(['gsutil', 'cp', 'gs://humann2_data/'+ unirefname,  '.'])
    else:
        download_file(unirefurl, os.path.join(unirefdir, unirefname))
    decompress_tar(os.path.join(unirefdir, unirefname), unirefdir)
    os.unlink(os.path.join(unirefdir, unirefname))

def run_metaphlan(sample_name, metaphlandb, output_path, ncores):
    metaphlandb = os.path.expandvars(metaphlandb)
    output_path = os.path.expandvars(output_path)
    for d in ['metaphlan', 'marker_abundance', 'marker_presence', 'metaphlan_bugs_list']:
        make_folder(os.path.join(output_path, d))
    
    try:
        sb.check_call(
        ['metaphlan',
        '--input_type', 'fastq','--index', 'latest',
        '--bowtie2db', metaphlandb,
        '--samout', os.path.join(output_path, 'metaphlan', '{}.sam.bz2'.format(sample_name)),
        '--bowtie2out',  os.path.join(output_path, 'metaphlan', '{}.bowtie2out'.format(sample_name)),
        '--nproc', str(ncores),
        '-o', os.path.join(output_path, 'metaphlan_bugs_list', '{}.tsv'.format(sample_name)),
        os.path.join(output_path, 'reads', '{}.fastq'.format(sample_name))])

        sb.check_call(
        ['metaphlan',
        '--input_type', 'bowtie2out','--index', 'latest',
        '--bowtie2db', metaphlandb,
        '-t', 'marker_pres_table',
        '-o', os.path.join(output_path, 'marker_presence', '{}.tsv'.format(sample_name)),
        os.path.join(output_path, 'metaphlan', '{}.bowtie2out'.format(sample_name))
        ])
        
        sb.check_call(
        ['metaphlan',
        '--input_type', 'bowtie2out', '--index', 'latest',
        '--bowtie2db', metaphlandb,
        '-t', 'marker_ab_table',
        '-o', os.path.join(output_path, 'marker_abundance', '{}.tsv'.format(sample_name)),
        os.path.join(output_path, 'metaphlan', '{}.bowtie2out'.format(sample_name))
        ])
    except sb.CalledProcessError as e:
        sys.exit(1)

def run_strainphlan(sample_name, output_path, ncores):
    output_path = os.path.expandvars(output_path)
    make_folder(os.path.join(output_path, 'consensus_markers'))
    
    try:
        sb.check_call([ 'sample2markers.py', 
                        '-i', os.path.join(output_path, 'metaphlan', '{}.sam.bz2'.format(sample_name)),
                        '-o', os.path.join(output_path, 'consensus_markers'),
                        '-n', str(ncores)]
                    )
    except sb.CalledProcessError as e:
        sys.exit(1)

def run_humann(sample_name, chocophlandir, unirefdir, metaphlandb, output_path, ncores):
    output_path = os.path.expandvars(output_path)
    metaphlandb = os.path.expandvars(metaphlandb)
    chocophlandir = os.path.expandvars(chocophlandir)
    unirefdir = os.path.expandvars(unirefdir)
    
    for d in ['humann','genefamilies','genefamilies_relab','genefamilies_cpm','pathabundance','pathabundance_relab','pathcoverage','pathabundance_cpm']:
        make_folder(os.path.join(output_path, d))
    
    try:
        sb.check_call([ 'humann',
                        '--input', os.path.join(output_path, 'reads', '{}.fastq'.format(sample_name)),
                        '--output', os.path.join(output_path,'humann'),
                        '--nucleotide-database', chocophlandir, 
                        '--taxonomic-profile', os.path.join(output_path, 'metaphlan_bugs_list', '{}.tsv'.format(sample_name)),
                        '--protein-database', unirefdir,
                        '--metaphlan-options', '"--bowtie2db {}"'.format(metaphlandb), 
                        '--threads', str(ncores)]
                    )
    except sb.CalledProcessError as e:
        sys.exit(1)
    
    shutil.move(os.path.join(output_path,'humann', '{}_genefamilies.tsv'.format(sample_name)), os.path.join(output_path, 'genefamilies', '{}.tsv'.format(sample_name)))
    shutil.move(os.path.join(output_path,'humann', '{}_pathabundance.tsv'.format(sample_name)), os.path.join(output_path, 'pathabundance', '{}.tsv'.format(sample_name)))
    shutil.move(os.path.join(output_path,'humann', '{}_pathcoverage.tsv'.format(sample_name)), os.path.join(output_path, 'pathcoverage', '{}.tsv'.format(sample_name)))

    sys.stdout.write('Normalizing HUMAnN output...\n')

    for norm in ['cpm', 'relab']:
        for input_type in ['genefamilies', 'pathabundance']:
            try:
                sb.check_call([ 'humann_renorm_table',
                                '--input', os.path.join(output_path, input_type, '{}.tsv'.format(sample_name)),
                                '--output', os.path.join(output_path, '{}_{}'.format(input_type, norm), '{}.tsv'.format(sample_name)),
                                '--units', norm]
                            )
            except sb.CalledProcessError as e:
                sys.exit('Failed to {} normalize {} file for sample {}'.format_map(norm, input_type, sample_name))