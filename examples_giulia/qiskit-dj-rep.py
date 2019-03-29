# useful additional packages
import numpy as np
from math import pi
import time
import argparse
import sys

#add command lines
#initiate the parser
text = 'This is the DJ (Quantum-) Algorithm.'
parser = argparse.ArgumentParser(description=text)
parser.add_argument("-n", "--numQubits", type=int, help="Input number of qubits / length of the boolean function")
parser.add_argument("-r", "--repetitions", type=int, help="Number of repetitions", default=1)
parser.add_argument("-thr", "--maxThreads", type=int, help="Maximal number of threads used", default=0)

args = parser.parse_args()

if not args.numQubits:
   print("Please specify the number of qubits / length of the boolean function, using the flag -n or --numQubits.")
   sys.exit()
else:
    n = int(args.numQubits)

nrep = int(args.repetitions)
maxThreads = int(args.maxThreads)


# importing Qiskit
from qiskit import BasicAer, IBMQ
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, compile
from qiskit.tools.visualization import circuit_drawer
from qiskit.tools.monitor import job_monitor

# import basic plot tools
from qiskit.tools.visualization import plot_histogram

#n = 13
# Choose a type of oracle at random. With probability half it is constant,
# and with the same probability it is balanced

#oracleType, oracleValue = np.random.randint(2), np.random.randint(2)
oracleType, oracleValue = 1, 1

if oracleType == 0:
    print("The oracle returns a constant value ", oracleValue)
else:
    print("The oracle returns a balanced function")
    a = np.random.randint(1, 2 ** n)  # this is a hidden parameter for balanced oracle.

# Choose backend
backend = BasicAer.get_backend('qasm_simulator')

mean_t = 0
mean_t2 = 0
mean_execute = 0
mean_execute2 = 0
for reps in range(nrep):
    # Creating registers
    # n qubits for querying the oracle and one qubit for storing the answer
    t = time.time()
    qr = QuantumRegister(n + 1)  # all qubits are initialized to zero
    # for recording the measurement on the first register
    cr = ClassicalRegister(n)

    circuitName = "DeutschJozsa"
    djCircuit = QuantumCircuit(qr, cr)

    # Create the superposition of all input queries in the first register by applying the Hadamard gate to each qubit.
    for i in range(n):
        djCircuit.h(qr[i])

    # Flip the second register and apply the Hadamard gate.
    djCircuit.x(qr[n])
    djCircuit.h(qr[n])

    # Apply barrier to mark the beginning of the oracle
    #djCircuit.barrier()

    if oracleType == 0:  # If the oracleType is "0", the oracle returns oracleValue for all input.
        if oracleValue == 1:
            djCircuit.x(qr[n])
        else:
            djCircuit.iden(qr[n])
    else:  # Otherwise, it returns the inner product of the input with a (non-zero bitstring)
        for i in range(n):
            if (a & (1 << i)):
                djCircuit.cx(qr[i], qr[n])

    # Apply barrier to mark the end of the oracle
    #djCircuit.barrier()

    # Apply Hadamard gates after querying the oracle
    for i in range(n):
      djCircuit.h(qr[i])

    # Measurement
    #djCircuit.barrier()
    for i in range(n):
        djCircuit.measure(qr[i], cr[i])

    #draw the circuit
    #djCircuit.draw(output='mpl')

    shots = 100
    t_execute = time.time()
    job = execute(djCircuit, backend=backend, shots=shots, backend_options={"max_parallel_threads": maxThreads})
    elapsed_execute = time.time() - t_execute
    results = job.result()
    answer = results.get_counts()
    elapsed = time.time() - t
    mean_t += elapsed
    mean_t2 += elapsed**2
    mean_execute += elapsed_execute
    mean_execute2 += elapsed_execute**2

mean_t /= nrep
mean_t2 /= nrep
mean_execute /= nrep
mean_execute2 /= nrep
std_t = np.sqrt(mean_t2-mean_t**2)
std_execute = np.sqrt(mean_execute2-mean_execute**2)
print("Answer = ", answer)
print("Avg elapsed time [ms] = ", mean_t*1e3, " Std deviation = ", std_t*1e3)
print("Job execute: Avg elapsed time [ms] = ", mean_execute*1e3, " Std deviation = ", std_execute*1e3)

#fig = plot_histogram(answer)

#fig.show()


