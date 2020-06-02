# Project management

See [zenhub project management](https://app.zenhub.com/workspaces/cmd-project-management-5e3d745411e3ced1cfa8fbe9/board?repos=116720695,58228080,95220777,250843441) across this and related repos.

# Pipeline project overview

Here is a high-level [slide deck](https://www.dropbox.com/s/tawgf4l49190m4o/2020-05-20%20intro%20to%20NCI%201U01%20CA230551%20.pptx?dl=0)

See the [wiki](https://github.com/waldronlab/curatedMetagenomicDataHighLoad/wiki/Environment-variables-and-invocation) for full setup and execution instructions.

# What is here

* a MetaPhlan3 + HUMAnN3 + StrainPhlAn + sratoolkit Docker image.  (see [docker directory](https://github.com/waldronlab/curatedMetagenomicDataHighLoad/tree/master/docker/curatedMetagenomics) for Dockerfile and link to Dockerhub). 
    - Instructions to run are kept in a [wiki](https://github.com/waldronlab/curatedMetagenomicDataHighLoad/wiki/Environment-variables-and-invocation). 
    - There is still work to be done turning bash scripts into a Python package with improved documentation, arguments, and versioning.

* a sratoolkit-only docker image (see [docker directory](https://github.com/waldronlab/curatedMetagenomicDataHighLoad/tree/master/docker/sratoolkit), but this is also included in the above all-in-one image. 
