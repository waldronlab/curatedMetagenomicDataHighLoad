# AWS Batch overview

- *Job* - A unit of work (a shell script, a Linux executable, or a
container image) that you submit to AWS Batch. It has a name, and runs
as a containerized app on EC2 using parameters that you specify in a
Job Definition. Jobs can reference other jobs by name or by ID, and
can be dependent on the successful completion of other jobs.

- *Job Definition* – Specifies how Jobs are to be run. Includes an AWS
Identity and Access Management (IAM) role to provide access to AWS
resources, and also specifies both memory and CPU requirements. The
definition can also control container properties, environment
variables, and mount points. Many of the specifications in a Job
Definition can be overridden by specifying new values when submitting
individual Jobs.

- *Job Queue* – Where Jobs reside until scheduled onto a Compute
Environment. A priority value is associated with each queue.

- *Scheduler* – Attached to a Job Queue, a Scheduler decides when, where,
and how to run Jobs that have been submitted to a Job Queue. The AWS
Batch Scheduler is FIFO-based, and is aware of dependencies between
jobs. It enforces priorities, and runs jobs from higher-priority
queues in preference to lower-priority ones when the queues share a
common Compute Environment. The Scheduler also ensures that the jobs
are run in a Compute Environment of an appropriate size.

- *Compute Environment* – A set of managed or unmanaged compute resources
that are used to run jobs. Managed environments allow you to specify
desired instance types at several levels of detail. You can set up
Compute Environments that use a particular type of instance, a
particular model such as c4.2xlarge or m4.10xlarge, or simply specify
that you want to use the newest instance types. You can also specify
the minimum, desired, and maximum number of vCPUs for the environment,
along with a percentage value for bids on the Spot Market and a target
set of VPC subnets. Given these parameters and constraints, AWS Batch
will efficiently launch, manage, and terminate EC2 instances as
needed. You can also launch your own Compute Environments. In this
case you are responsible for setting up and scaling the instances in
an Amazon ECS cluster that AWS Batch will create for you.


# Custom AMI

The AMI used by default in ECS (batch) is too small (22GB disk). Follow instructions here:

https://github.com/nextflow-io/nextflow/blob/master/docs/awscloud.rst#custom-ami




# Examples

## Fetch and Run

This is an example of using AWS batch to run a shell script:

https://aws.amazon.com/blogs/compute/creating-a-simple-fetch-and-run-aws-batch-job/

### Build image

In the `fetch_and_run` directory....


```
docker build -t fetch_and_run
docker push seandavi/fetch_and_run
```

### Copy job script to s3

```
export BUCKET=curatedmetagenomics.bioconductor.org
aws s3 cp myjob.sh s3://$BUCKET/aws_batch/fetch_and_run_example/myjob.sh
```

### Create IAM role that can access s3

The IAM role that runs the container must have access to s3 in order to access
the script. Create an `Elastic Container Role` and add permissions to 
`AmazonS3ReadOnly` or `AmazonS3FullAccess` (for writing, later).

### Create job description

See https://aws.amazon.com/blogs/compute/creating-a-simple-fetch-and-run-aws-batch-job/

### Create job

See https://aws.amazon.com/blogs/compute/creating-a-simple-fetch-and-run-aws-batch-job/

Note the use of environment variables....

