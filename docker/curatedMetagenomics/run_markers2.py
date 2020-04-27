#!/usr/bin/env python

import os
import glob
import sys
import argparse 
import multiprocessing
import subprocess

def read_params():
    p = argparse.ArgumentParser()
    p.add_argument('--metaphlan_db_name', required=False, 
                   default='mpa_v30_CHOCOPhlAn_201901',
                   type=str)
    p.add_argument('--bt2_ext', required=False,
                   default='.bowtie2_out.bz2',
                   type=str)
    p.add_argument('--input_dir', required=True, type=str)
    p.add_argument('--output_dir', required=True, type=str)
    p.add_argument('--nprocs', required=True, type=int)
    p.add_argument('--params', required=False, default='', type=str)

    return vars(p.parse_args())

def run(cmd):
    print(cmd)
    subprocess.check_call(cmd.split(' '))

def run_markers(args):
    metaphlan_db_name = args['metaphlan_db_name']
    input_dir = args['input_dir']
    bt2_ext = args['bt2_ext']
    nprocs = args['nprocs']
    params = args['params']
    output_dir = args['output_dir']
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    cmds = []
    ifns = sorted(glob.glob('%s/*%s'%(input_dir, bt2_ext)))
    for ifn in ifns:
        for ana_type in ['rel_ab', 'marker_pres_table', 'marker_ab_table']:
            ofn = ifn.replace(bt2_ext, '.%s'%ana_type)
            cmd = 'metaphlan --mpa_pkl {} --input_type bowtie2out {} -o '.format(metaphlan_db_name, ifn, ofn)
            if not os.path.isfile(ofn):
                cmds.append(cmd)

            base_ofn = os.path.basename(ifn).replace(bt2_ext, '.%s'%ana_type)
            ofn = os.path.join(output_dir, base_ofn)
            cmd = 'metaphlan --mpa_pkl {} --input_type bowtie2out {} {} -o '.format(metaphlan_db_name, params, ifn, ofn)
            if not os.path.isfile(ofn):
                cmds.append(cmd)

    with multiprocessing.Pool(nprocs) as pool:
        pool.imap_unordered(run, cmds)

if __name__ == "__main__":
    args = read_params()
    run_markers(args)
