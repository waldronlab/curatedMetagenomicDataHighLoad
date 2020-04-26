#!/usr/bin/env python

import os
import glob
import sys
import argparse 
import multiprocessing

def read_params():
    p = argparse.ArgumentParser()
    p.add_argument('--metaphlan_db', required=False, 
                   default='metaphlan/db_v30_CHOCOPhlAn_201901/mpa_v30_CHOCOPhlAn_201901.pkl',
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
    print cmd
    os.system(cmd)

def run_markers(args):
    metaphlan_db = args['metaphlan_db']
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
            cmd = 'metaphlan --mpa_pkl {} --input_type bowtie2out {} -o '.format(metaphlan_db, ifn, ofn)
            if not os.path.isfile(ofn):
                cmds.append(cmd)

            base_ofn = os.path.basename(ifn).replace(bt2_ext, '.%s'%ana_type)
            ofn = os.path.join(output_dir, base_ofn)
            cmd = 'metaphlan --mpa_pkl {} --input_type bowtie2out {} {} -o '.format(metaphlan_db, params, ifn, ofn)
            if not os.path.isfile(ofn):
                cmds.append(cmd)

    with multiprocessing.Pool(nprocs) as pool:
        pool.imap_unordered(run, cmds)

if __name__ == "__main__":
    args = read_params()
    run_markers(args)
