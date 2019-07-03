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
Assertion of product states.
"""
from qiskit.circuit.instruction import Instruction
from qiskit.circuit.measure import Measure
from qiskit.assertions.assertmanager import AssertManager
from qiskit.assertions.asserts import Asserts
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.exceptions import QiskitError
from scipy.stats import chi2_contingency

class AssertProduct(Asserts):
    """
        Assertion of product states and quantum measurement
        in the computational basis.
    """
    def __init__(self, qubit0, cbit0, qubit1, cbit1, expval, pcrit): #qubit&cbit lists here
        super().__init__()
        self._type = "Product"
        self._qubit0 = qubit0
        self._cbit0 = cbit0
        self._qubit1 = qubit1
        self._cbit1 = cbit1
        self._pcrit = pcrit
        self._expval = expval

    def stat_test(self, counts):
        #vals_list = list(counts.values())
        #numzeros = 2**len(list(counts)[0]) - len(counts)
        #vals_list.extend([0]*numzeros)
        # numshots = sum(list(counts.values()))
        
        q0len = len(self._qubit0)
        q1len = len(self._qubit1)
        #empty contingency table with right dimensions
        cont_table = [[0]*q0len] *q1len
        for (key, value) in counts:
            q0index = key[:q0len]
            q1index = key[q0len:q1len+1]
            cont_table[q1index][q0index] = value

        """try:
            index = list(map(int, counts.keys())).index(self._expval)
        except ValueError:
            index = -1
        exp_list[index] = 2**16
        """

        print("cont_table")
        print(cont_table)
        chisq, pval = (chi2_contingency(cont_table))
        print("chisq, pval = ")
        print(chisq, pval)
        if pval <= self._pcrit:
            passed = True
        else:
            passed = False
        return (chisq, pval, passed)


def assertproduct(self, expval, pcrit, qubit0, cbit0, qubit1, cbit1):
    """Create product assertion

    Args:
        expval: integer of 0's and 1's
        pcrit: critical p-value for the hypothesis test
        qubit0 (QuantumRegister|list|tuple): quantum register
        cbit0 (ClassicalRegister|list|tuple): classical register
        qubit1 (QuantumRegister|list|tuple): quantum register
        cbit1 (ClassicalRegister|list|tuple): classical register

    Returns:
        qiskit.QuantumCircuit: copy of quantum circuit at the assert point.

    Raises:
        QiskitError: if qubit is not in this circuit or bad format;
            if cbit is not in this circuit or not creg.
    """
    theClone = self.copy("breakpoint"+"_"+AssertManager.breakpoint_name())
    AssertManager.StatOutputs[theClone.name] = {"type":"Product","qubit0":qubit0,"cbit0":cbit0, "qubit1":qubit1, "cbit1":cbit1}
    theClone.append(AssertProduct(qubit0, cbit0, qubit1, cbit1, expval, pcrit), [qubit0.extend(qubit1)], [cbit0.extend(cbit1)])
    return theClone

QuantumCircuit.assertproduct = assertproduct
