#!/bin/bash -l

# this part will be ignored if:
# - nodes are preallocated with salloc
# - and the file is executed as just run.sh (not sbatch run.sh)
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --constraint=mc
#SBATCH --partition=normal
#SBATCH --time=400

# loading necessary modules
echo "============================="
echo "  LOADING MODULES"
echo "============================="
module load daint-mc
module load cray-python/3.6.5.1
module load PyExtensions/3.6.5.1-CrayGNU-18.08
source $SCRATCH/g_virtenv/bin/activate

export CRAYPE_LINK_TYPE=dynamic

echo "================================"
echo "       RUNNING BENCHMARKS"
echo "================================"

nodes=1
ranks_per_node=1

n_repetitions=10
N=(4 7 10 13 16 19 22 25)
threads_per_rank=(1 2 4 8 16 32)

cd ../examples_giulia/
#path_to_executable="../examples_giulia/qiskit-dj.py"

# iterate over the values of argument N
for arg in "${N[@]}"
do
    # iterate over the values of threads
    for threads in "${threads_per_rank[@]}"
    do
        export OMP_NUM_THREADS=${threads}

        echo "CONFIGURATION: N = ${arg}, threads = ${threads}"
        echo "CONFIGURATION: N = ${arg}, threads = ${threads}" >> ../docs/dj-benchmark-rep.txt

        output=$(srun -u -N $nodes --ntasks-per-node=$ranks_per_node python qiskit-dj-rep.py -n ${arg} -r ${n_repetitions} -thr ${threads})
        echo "$output" >> ../docs/dj-benchmark-rep.txt
        echo "--------------------------------" >> ../docs/dj-benchmark-rep.txt
    done
    echo ""
    echo "================================"
    echo ""
done

deactivate

