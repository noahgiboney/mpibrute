# mpibrute

This simulation is a extension of a Cal Poly CSC321 (Introduction to Computer Security) assignment, where the goal is to crack provided password hashes (that have an increased level of salt as the program progresses)

## How it works

mpibrute uses MPI (message passing interface) and Slurm workload manager to take advantage of mass parallization on a high performance computing cluster.

The program uses a set of common words to compare against a set of hashed passwords. 

The amount of parallel work that can be done depends on the values set in `mpibrute.sh` which is a SBATCH file. Here we can define the amount of nodes, number of tasks we want to span per node. Those values will determine how mnay MPI ranks we get to run with.

MPI is used to communicate between the ranks, for things such as broadcasting the word list, and notify other ranks when one has found the password.

`mpibrute` is launched with as a Slurm batch command.
`sbatch mpibrute.sh`

## Results