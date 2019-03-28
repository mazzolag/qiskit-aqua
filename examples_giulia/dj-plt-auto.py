import matplotlib.pyplot as plt
import numpy as np

threads = [1, 2, 4, 8, 16, 32]  # number of threads
numQubits = [4, 7, 10, 13, 16, 19]  # input number n

# readout data from textfile
filenames = ["../docs/dj-bench.txt"]
master_data = []
data = [master_data]

for i, filename in enumerate(filenames):
    f = open(filename, 'r')
    data[i] = f.read()
    f.close()

    temp = data[i].split('\n')

    avg_times = [row.split(' ')[5] for row in temp if row.startswith("elapsed")]
    avg_times = [k.split('^M')[0] for k in avg_times]  # get rid of the '^M' in the list of avg_times

    avg_times = [float(num) for num in avg_times]
    lenThr = len(threads)
    print(avg_times)
    y = []
    for j in range(len(numQubits)):
        y.append(avg_times[j*lenThr:(j*lenThr + lenThr)])

plt.figure()
dimx = int(np.round(np.sqrt(len(y))))
dimy = dimx if dimx*dimx >= len(y) else dimx+1
for i in range(len(y)):
    plt.subplot(dimx, dimy, i+1)
    #y[i] = [x*1e-6 for x in y[i]]
    plt.semilogx(threads, y[i], basex=2, linestyle='dashed', marker='.', markerfacecolor='black', markersize=7, label="n = %a " % (numQubits[i]))
    plt.xlabel('number of threads')
    plt.ylabel('time [ms]')
    plt.legend(loc='upper left')
plt.suptitle('benchmark for DJ algortihm in qiskit')
plt.tight_layout()
plt.subplots_adjust(top=0.86)
plt.savefig('dj-benchmark')
plt.show()
