from qiskit.circuit.library.standard_gates import XGate, YGate, ZGate, IGate, PhaseGate
from qiskit.quantum_info.operators import Operator
from qiskit import QuantumCircuit, Aer, transpile, assemble
import numpy as np
from py_functions.SP import State_Preparation as sp

class Select:

    def give_pauli(str):

        if str == 'I':
            return np.array([[1,0],[0,1]])
        elif str == 'X':
            return np.array([[0,1],[1,0]])
        elif str == 'Y':
            return np.array([[0, -1j],[1j,0]])
        elif str == 'Z':
            return np.array([[1,0],[0,-1]])
        else:
            init = 1
            for i in str:
                if init == 1:
                    matrix = Select.give_pauli(i)
                    init = 2
                else:
                    matrix = np.kron(matrix, Select.give_pauli(i))
            return matrix
        
    def give_phase(value):
        if value == 0:
            return 0
        elif isinstance(value, complex):
            if value.imag == 0:
                if value.real < 0:
                    return np.pi
                else:
                    return 0
            else:
                if value.imag > 0:
                    return np.pi / 2
                elif value.imag < 0:
                    return -np.pi / 2
        elif isinstance(value, (int, float)):
            if value < 0:
                return np.pi
            else:
                return 0
        else:
            return None
        
    def select_circuit(matrix_info):

        keys = list(matrix_info.keys())
        num_qubits = len(keys[0])
        num_control_qubits = int(np.log2(len(keys)))

        qc_select = QuantumCircuit(int(num_qubits+num_control_qubits), name="Select")

        number_logic = 0 # variable to apply the xgates to the control unitaries.

        for i in matrix_info.keys():
            qc_aux = QuantumCircuit(num_qubits, name=" {}  ".format(i))
            opt = Operator(Select.give_pauli(i))
            qc_aux.unitary(opt, list(np.arange(0,num_qubits)))
            Ui = qc_aux.control(num_control_qubits)

            binary_number = '{0:b}'.format(number_logic).zfill(num_control_qubits)

            ######## Circuit Implementation
            ### Logic implementation
            iter = 0
            for j in binary_number:
                if j == '0':
                    qc_select.x(iter)
                iter = iter + 1

            #### Add the quantum operator
            P = PhaseGate(Select.give_phase(matrix_info[i])).control(num_control_qubits-1)
            qc_select.append(P, list(np.arange(0, num_control_qubits)))
            qc_select.append(Ui, list(np.arange(0, num_qubits+num_control_qubits)))

            ### Logic implementation inverse
            iter = 0
            for j in binary_number:
                if j == '0':
                    qc_select.x(iter)
                iter = iter + 1

            ######## Finish implemention
            qc_select.barrier()

            number_logic = number_logic + 1
        
        return qc_select
        
    
    
