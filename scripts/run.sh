#!/bin/bash -l

# this part will be ignored if:
# - nodes are preallocated with salloc
# - and the file is executed as just run.sh (not sbatch run.sh)
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=2
#SBATCH --constraint=mc
#SBATCH --partition=normal
#SBATCH --time=30

# loading necessary modules
echo "============================="
echo "  LOADING MODULES"
echo "============================="
module load daint-mc
module load python_virtualenv/15.0.3
module load cray-python
module load CMake

export CRAYPE_LINK_TYPE=dynamic

echo "================================"
echo "       RUNNING BENCHMARKS"
echo "================================"

nodes=1
ranks_per_node=1

n_repetitions=3
N=(4 7 10 13 16 19 21 24 27)
threads_per_rank=(1 2 4 8 16 32)

path_to_executable="./examples_giulia/shor"

# iterate over the values of argument N
for arg in "${N[@]}"
do
    # iterate over the values of threads
    for threads in "${threads_per_rank[@]}"
    do
        export OMP_NUM_THREADS=${threads}

        echo "CONFIGURATION: N = ${arg}, threads = ${threads}"

        output=$(srun -u -N $nodes --ntasks-per-node=$ranks_per_node ${path_to_executable} -N ${arg} -r ${n_repetitions})
        echo "$output"
        echo "--------------------------------"
    done
    echo ""
    echo "================================"
    echo ""
done

