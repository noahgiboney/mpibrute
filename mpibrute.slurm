#!/bin/bash

# Run with `sbatch mpibrute.slurm` on a cluster with slurm and openmpi installed.

TASKS_PER_NODE=1
NODES=1

OUTPUT_FILE="mpibrute_n${TASKS_PER_NODE}_N${NODES}"

#SBATCH --job-name=mpibrute
#SBATCH --output=${OUTPUT_FILE}.log
#SBATCH --error=${OUTPUT_FILE}.error
#SBATCH --partition=<partition_name> # Replace with partition name
#SBATCH --nodes=${NODES}
#SBATCH --ntasks-per-node=${TASKS_PER_NODE}
#SBATCH --cpus-per-task=1

srun python3 mpibrute.py