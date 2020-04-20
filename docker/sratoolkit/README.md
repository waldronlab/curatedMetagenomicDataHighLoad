Built at https://hub.docker.com/repository/docker/waldronlab/sratoolkit

Try (from [here](https://github.com/waldronlab/curatedMetagenomicDataHighLoad/blob/d75292260c1f9d944e8c16bb39b907ed297b03ad/docker/curatedMetagenomics/curatedMetagenomicData_pipeline.sh#L54)):

For all runs of this sample use `runs="SRR2244401;SRR2236793;SRR2243639;SRR2243812;SRR2244215;SRR2245587;SRR2228273;SRR2228283;SRR2228304;SRR2228308;SRR2228313;SRR2228320;SRR2228347;SRR2228399;SRR2226903;SRR2226948;SRR2227815;SRR2228028;SRR2228363;SRR2228450;SRR2228455;SRR2228709"`

```
sample="M1.1.SA"
runs="SRR2244401;SRR2236793"
mkdir reads
fastq-dump --outdir reads ${runs}
echo 'Downloaded.'
echo 'Concatenating runs...'
cat reads/*.fastq > reads/${sample}.fastq
ls -l reads/
```
