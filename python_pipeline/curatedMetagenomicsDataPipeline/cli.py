#!/usr/bin/env python3
import click
from .utils import download_file as _download_file
from .utils import download_metaphlan_databases as _download_metaphlan_databases
from .utils import download_chocophlan as _download_chocophlan
from .utils import download_uniref as _download_uniref
from .utils import run_metaphlan as _run_metaphlan
from .utils import run_strainphlan as _run_strainphlan
from .utils import run_humann as _run_humann

@click.group(help="Command-line suite utilities for curatedMetagenomicsData")
def cmd_cli():
    pass

@cmd_cli.group(help="Commands for downloading databases")
def download():
    pass

@download.command('download_file', help='Download a file in a choosen destination')
@click.argument('url')
@click.argument('file_path')
def download_file(url, file_path):
    _download_file(url, file_path)

@download.command('metaphlan_database', help='Download and install the latest available MetaPhlAn database')
@click.argument('metaphlandb', envvar='metaphlandb', type=click.Path())
def download_metaphlan_databases(metaphlandb):
    _download_metaphlan_databases(metaphlandb)

@download.command('chocophlan', help='Download annotated CHOCOPhlAn pangenomes')
@click.argument('chocophlandir', envvar='chocophlandir')
@click.argument('chocophlanname', envvar='chocophlanname')
@click.argument('chocophlanurl', envvar='chocophlanurl')
def download_chocophlan(chocophlandir, chocophlanname, chocophlanurl):
    _download_chocophlan(chocophlandir, chocophlanname, chocophlanurl)

@download.command('uniref', help='Download UniRef database')
@click.argument('unirefdir', envvar='unirefdir')
@click.argument('unirefname', envvar='unirefname')
@click.argument('unirefurl', envvar='unirefurl')
def download_uniref(unirefdir, unirefname, unirefurl):
    _download_uniref(unirefdir, unirefname, unirefurl)

@cmd_cli.group(help="Commands for running profiling tools")
def run():
    pass

@run.command('metaphlan', help='Run MetaPhlAn on a sample')
@click.argument('sample_name')
@click.argument('metaphlandb', envvar='metaphlandb')
@click.argument('output_path', envvar='output_path')
@click.argument('ncores', envvar='ncores', default=2, type=click.INT)
def run_metaphlan(sample_name, metaphlandb, output_path, ncores):
    _run_metaphlan(sample_name, metaphlandb, output_path, ncores)

@run.command('strainphlan', help='Run StrainPhlAn on a sample')
@click.argument('sample_name')
@click.argument('output_path', envvar='output_path')
@click.argument('ncores', envvar='ncores', default=2, type=click.INT)
def run_strainphlan(sample_name, output_path, ncores):
    _run_strainphlan(sample_name, output_path, ncores)

@run.command('humann', help='Run HUMAnN on a sample')
@click.argument('sample_name')
@click.argument('chocophlandir', envvar='chocophlandir')
@click.argument('unirefdir', envvar='unirefdir')
@click.argument('metaphlandb', envvar='metaphlandb')
@click.argument('output_path', envvar='output_path')
@click.argument('ncores', envvar='ncores', default=2, type=click.INT)
def run_humann(sample_name, chocophlandir, unirefdir, metaphlandb, output_path, ncores):
    _run_humann(sample_name, chocophlandir, unirefdir, metaphlandb, output_path, ncores)

if __name__ == '__main__':
    cmd_cli()