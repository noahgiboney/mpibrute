#!/bin/bash

#SBATCH --job-name=mpibrute
#SBATCH --output=mpibrute_n256_n10.log
#SBATCH --error=mpibrute_n256_n10.error
#SBATCH --partition=antero
#SBATCH --nodes=10
#SBATCH --ntasks-per-node=256
#SBATCH --cpus-per-task=1

srun python3 mpibrute.py