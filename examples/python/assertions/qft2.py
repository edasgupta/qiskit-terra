# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Quantum Fourier Transform examples.
"""

import math
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import execute, BasicAer
from qiskit.assertions.asserts import Asserts
from qiskit.assertions.assertmanager import AssertManager

###############################################################
# make the qft
###############################################################
def input_state(circ, n):
    """n-qubit input state for QFT that produces output 1."""
    for j in range(n):
        circ.h(j)
        circ.u1(-math.pi/float(2**(j)), j)

def qft(circ, n):
    """n-qubit QFT on q in circ."""
    for j in range(n):
        for k in range(j):
            circ.cu1(math.pi/float(2**(j-k)), j, k)
        circ.h(j)

q = QuantumRegister(3, 'q')
c = ClassicalRegister(3, 'c')
qft3 = QuantumCircuit(q, c, name="qft3")

# Below, qft3 is a 3-qubit quantum circuit.
input_state(qft3, 3) # Initializes the state so that post-QFT, the state should be 1.
# Insert a breakpoint to the qft3 circuit after initializing the input state.
# This asserts that the 3 qubits are in superposition, with critical p-value 0.05.
breakpoint1 = qft3.assertsuperposition(0.05, q, c)
qft3.barrier()
qft(qft3, 3)
qft3.barrier()

# Insert a breakpoint after the quantum Fourier Transform has been performed.
# This asserts that the qubits are a classical value of 1, with critical p-value 0.05.
breakpoint2 = qft3.assertclassical(1, 0.05, [q[0], q[1]], [c[0], c[1]])
for j in range(3):
    qft3.measure(j, j)

# setting up the backend, running the breakpoint and the job
sim_backend = BasicAer.get_backend('qasm_simulator')
job = execute([breakpoint1, breakpoint2, qft3], sim_backend, shots=1024)
result = job.result()

# We obtain a dictionary of the results from each of our statistical tests
# The line below also prints to command line whether the assertion passed or failed.
stat_outputs = AssertManager.stat_collect([breakpoint1, breakpoint2], result)
print("Full results of our assertion:")
print(stat_outputs)

# Show the results
print(result.get_counts(qft3))
