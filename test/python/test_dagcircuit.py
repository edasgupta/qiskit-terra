# -*- coding: utf-8 -*-

# Copyright 2017, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

# pylint: disable=invalid-name,missing-docstring

"""Test for the DAGCircuit object"""

import unittest

from qiskit.dagcircuit import DAGCircuit

from .common import QiskitTestCase


class TestDagCircuit(QiskitTestCase):
    """QasmParser"""
    def setUp(self):
        self.QASM_FILE_PATH = self._get_resource_path('qasm/example.qasm')

    def test_create(self):
        qubit0 = ('qr', 0)
        qubit1 = ('qr', 1)
        clbit0 = ('cr', 0)
        clbit1 = ('cr', 1)
        condition = None
        dag = DAGCircuit()
        dag.add_basis_element('h', 1, number_classical=0, number_parameters=0)
        dag.add_basis_element('cx', 2)
        dag.add_basis_element('x', 1)
        dag.add_basis_element('measure', 1, number_classical=1,
                              number_parameters=0)
        dag.add_qreg('qr', 2)
        dag.add_creg('cr', 2)
        dag.apply_operation_back('h', [qubit0], [], [], condition)
        dag.apply_operation_back('cx', [qubit0, qubit1], [],
                                 [], condition)
        dag.apply_operation_back('measure', [qubit1], [clbit1], [], condition)
        dag.apply_operation_back('x', [qubit1], [], [], ('cr', 1))
        dag.apply_operation_back('measure', [qubit0], [clbit0], [], condition)
        dag.apply_operation_back('measure', [qubit1], [clbit1], [], condition)


if __name__ == '__main__':
    unittest.main()
