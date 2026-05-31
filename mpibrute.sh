#!/bin/bash

# Run with `sbatch mpibrute.sh` on a cluster with slurm and openmpi installed.

#SBATCH --job-name=mpibrute
#SBATCH --output=mpibrute_%j.log
#SBATCH --error=mpibrute_error_%j.log
#SBATCH --partition=<partition_name>
#SBATCH --nodes=<nodes>
#SBATCH --ntasks-per-node=<tasks_per_node>
#SBATCH --cpus-per-task=1

module load python/3.11
module load openmpi 

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

srun python mpibrute.py