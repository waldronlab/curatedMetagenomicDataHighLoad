# Project management

See [zenhub project management](https://app.zenhub.com/workspaces/cmd-project-management-5e3d745411e3ced1cfa8fbe9/board?repos=116720695,58228080,95220777,250843441) across this and related repos.

# Pipeline project overview

Here is a high-level [slide deck](https://www.dropbox.com/s/tawgf4l49190m4o/2020-05-20%20intro%20to%20NCI%201U01%20CA230551%20.pptx?dl=0)

See the [wiki](https://github.com/waldronlab/curatedmetagenomics/wiki/Environment-variables-and-invocation) for full setup and execution instructions.

# What is here

## MetaPhlan3 + HUMAnN3 + StrainPhlAn + sratoolkit Docker+Singularity images

| DockerHub    | SingularityHub      |
|-	       |-		     |
| [![](https://images.microbadger.com/badges/version/waldronlab/curatedmetagenomics.svg)](https://hub.docker.com/repository/docker/waldronlab/curatedmetagenomics)		| [![https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg](https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg)](https://singularity-hub.org/collections/4365) |

(see [docker directory](https://github.com/waldronlab/curatedmetagenomics/tree/master/docker/curatedMetagenomics) for Dockerfile and link to Dockerhub). 
    - Instructions to run are kept in a [wiki](https://github.com/waldronlab/curatedmetagenomics/wiki/Environment-variables-and-invocation). 
    - There is still work to be done turning bash scripts into a Python package with improved documentation, arguments, and versioning.

## sratoolkit-only Docker+Singularity images 

| DockerHub 	| SingularityHub 	|
|-	|-	|
| [![](https://images.microbadger.com/badges/version/waldronlab/sratoolkit.svg)](https://hub.docker.com/repository/docker/waldronlab/sratoolkit)         	| [![https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg](https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg)](https://singularity-hub.org/collections/4458) |

(see [docker directory](https://github.com/waldronlab/curatedmetagenomics/tree/master/docker/sratoolkit), but this is also included in the above all-in-one image. 

* a PyPi project for the curatedmetagenomics pipeline

See the [python_pipeline](https://github.com/waldronlab/curatedmetagenomics/tree/master/python_pipeline) directory
