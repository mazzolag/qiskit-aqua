# useful additional packages
import numpy as np
import matplotlib.pyplot as plt
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

args = parser.parse_args()

if not args.numQubits:
   print("Please specify the number of qubits / length of the boolean function, using the flag -n or --numQubits.")
   sys.exit()
else:
    n = int(args.numQubits)

nrep = int(args.repetitions)


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
oracleType, oracleValue = np.random.randint(2), np.random.randint(2)

if oracleType == 0:
    print("The oracle returns a constant value ", oracleValue)
else:
    print("The oracle returns a balanced function")
    a = np.random.randint(1, 2 ** n)  # this is a hidden parameter for balanced oracle.

# Creating registers
# n qubits for querying the oracle and one qubit for storing the answer
qr = QuantumRegister(n + 1)  # all qubits are initialized to zero
# for recording the measurement on the first register
cr = ClassicalRegister(n)

circuitName = "DeutschJozsa"
djCircuit = QuantumCircuit(qr, cr)

# Create the superposition of all input queries in the first register by applying the Hadamard gate to each qubit.

djCircuit.h(qr)

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
djCircuit.h(qr)

# Measurement
#djCircuit.barrier()
for i in range(n):
    djCircuit.measure(qr[i], cr[i])

#draw the circuit
djCircuit.draw(output='mpl')

#time management

backend = BasicAer.get_backend('qasm_simulator')
shots = nrep
t = time.time()
job = execgitute(djCircuit, backend=backend, shots=shots)
elapsed = time.time() - t
results = job.result()
answer = results.get_counts()
print("Answer = ", answer)
print("elapsed time [ms] = ", elapsed*1e3/nrep)

fig = plot_histogram(answer)

fig.show()


