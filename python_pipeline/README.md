## Installation

From PyPi:
```
pip install curatedmetagenomicspipeline
```

From source code:
```
git clone git@github.com:waldronlab/curatedmetagenomics.git
cd python_pipeline
pip install .
```

## Usage

```
cmd_pipeline --demo TEST_SAMPLE ERR262957 /output
```
The `--demo` argument causes use of a small demo FASTQ file and mini ChocoPhlAn, and UniRef databases (although ERR262957 is still downloaded to test `fasterq-dump`


```
cmd_pipeline MV_FEI4_t1Q14 "SRR4052038" /output
```

The command above download the specified SRR run for sample `MV_FEI4_t1Q14` from the AsnicarF_2017 dataset. Reads are then processed for:

- Taxonomic profiling with MetaPhlAn 3.0
  - Markers abundance and presence profiles are computed alongside the species-level profiling
- Strain-level profiling with StrainPhlAn 3.0 (only the consensus_marker step is done)
- Functional potential profiling with HUMAnN 3.0
  - Pathways and gene families abundances are normalized using species' relative abundances and CPM

For the full list of options and commands, please run `cmd_utilities_cli --help` and/or `cmd_utilities_cli COMMAND --help`
