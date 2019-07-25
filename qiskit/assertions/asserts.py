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
Abstract class and all derived classes for making statistical assertions.
"""
import abc
from qiskit.circuit.register import Register
from qiskit.circuit.classicalregister import ClassicalRegister, Clbit
from qiskit.circuit.instruction import Instruction
from qiskit.circuit.measure import Measure
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.exceptions import QiskitError
from scipy.stats import chisquare
from datetime import datetime

class Asserts(Measure):
    """A superclass for all assertions, and a subclass of Measure"""
    __metaclass__ = abc.ABCMeta

    def __init__(self, qubit, cbit, pcrit, negate):
        super().__init__()
        self._qubit = qubit
        self._cbit = cbit
        self._pcrit = pcrit
        self._negate = negate
        self._expval = None

    def breakpoint_name():
        """
        Returns the name of the breakpoint.  A breakpoint is a QuantumCircuit
        whose last instruction is an assertion instruction.

        Returns:
            string: the breakpoint name
        """
        return "breakpoint_" + datetime.now().isoformat()

    def syntax4measure(self, bit):
        """
        Returns the input qubit or cbit, suitable for the syntax of the measure
        instruction, as a list.

        Args:
            bit(QuantumRegister|ClassicalRegister|list|tuple): quantum or classical register

        Returns:
            list: bit as a list
        """
        if isinstance(bit,(list, Register)):
            return bit
        elif isinstance(bit,(range, tuple)):
            return list(bit)
        else: #if single bit
            return [bit]

    def clbits2idxs(cbits, exp):
        """
        Returns the indices of cbits with respect to exp, the QuantumCircuit.

        Args:
            cbits(ClassicalRegister|list|tuple): cbit of a measurement instruction
            exp(QuantumCircuit): an experiment

        Returns:
            list|range: the indices
        """
        if isinstance(cbits[0], int):
            return cbits
        elif isinstance(cbits[0], Clbit):
            idxs = [exp.clbits.index(cbit) for cbit in cbits]
            return idxs
        elif isinstance(cbits, ClassicalRegister):
            idxfirst = exp.clbits.index(cbits[0])
            idxlast = exp.clbits.index(cbits[-1])
            return range(idxfirst, idxlast+1)

    @abc.abstractmethod
    def stat_test(self, counts):
        """
        Abstract method which performs a statistical test on the experimental outcomes

        Args:
            counts(dictionary): result.get_counts(experiment)

        Returns:
            tuple: tuple containing:

                chisq(float): the chi-squared value
                pval(float): the p-value
                passed(Boolean): if the test passed
        """
        return
