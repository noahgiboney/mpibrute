# mpibrute

This simulation is a extension of a Cal Poly CSC321 (Introduction to Computer Security) assignment, where the goal is to crack provided password hashes (that have an increased level of salt as the program progresses)

## How it works

mpibrute uses MPI (message passing interface) and Slurm workload manager to take advantage of mass parallization on a high performance computing cluster.

The program uses a set of common words to compare against a set of hashed passwords. 

The amount of parallel work that can be done depends on the values set in `mpibrute.sh` which is a SBATCH file. Here we can define the amount of nodes, number of tasks we want to span per node. Those values will determine how many MPI ranks we get to run with.

MPI is used to communicate between the ranks, for things such as broadcasting the word list, and notify other ranks when one has found the password.

`mpibrute` is launched with as a Slurm batch command.
```
sbatch mpibrute.sh
```

## Results

Result of running `mpibrute` on an HPC cluster with MPI installed, launched with slurm.
```
Running with 1200 ranks
Bilbo: welcome 0.53s
Gandalf: wizard 0.36s
Thorin: diamond 0.51s
Fili: desire 1.13s
Kili: ossify 2.64s
Balin: hangout 4.71s
Dwalin: drossy 4.56s
Oin: ispaghul 3.70s
Gloin: oversave 4.19s
Dori: indoxylic 3.57s
Nori: swagsman 9.11s
Ori: airway 14.25s
Bifur: corrosible 10.29s
Bofur: libellate 3.56s
Durin: purrone 44.13s
```

Result of running the simulation on an m3 macbook pro using python concurrenty (no MPI & Slurm).
```
Bilbo: welcome 57.61 seconds
Gandalf: wizard 16.72 seconds
Thorin: diamond 135.25 seconds
Fili: desire 273.12 seconds
Kili: ossify 345.11 seconds
Balin: hangout 563.97 seconds
Dwalin: drossy 104.66 seconds
Oin: ispaghul 222.35 seconds
Gloin: oversave 6.91 seconds
Dori: indoxylic 645.93 seconds
Nori: swagsman 768.05 seconds
Ori: airway 2150.16 seconds
Bifur: corrodible 197.83 seconds
Bofur: libellate 2474.79 seconds
Durin: purrone 2086.85 seconds
```