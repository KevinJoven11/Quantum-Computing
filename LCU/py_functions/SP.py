import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.circuit.library.standard_gates import RYGate
from qiskit.visualization import plot_histogram
import math
import qiskit.quantum_info as qi
from sklearn.preprocessing import normalize

class State_Preparation:

    def gen_angles(x):
        """ This function give the angles for state preparation given 
            a set on probabilities in the quantum circuit.
            input:
                x : list = array of probabilities for the state.append
            output:
                angles: angles for the quantum circuit.

            Example:
                x = [np.sqrt(0.5),np.sqrt(0.2),np.sqrt(0.1),np.sqrt(0.3)]
            Where:
                0.5+0.2+0.1+0.3 = 1
            Output:
                array([1.2945, 1.1278, 2.0943])
        """

        angles = np.zeros(int(len(x)/2))
        if len(x)>1:
            new_x = np.zeros(int(len(x)/2))

            for k in range(0, len(new_x)):
                new_x[k] = np.sqrt(np.abs(x[2*k])**2+np.abs(x[2*k+1])**2)

            inner_angles = State_Preparation.gen_angles(new_x)
            angles = np.zeros(int(len(x)/2))
            
            for k in range(0, len(new_x)):
                if new_x[k] != 0:
                    if x[2*k] > 0:
                        angles[k] = 2*np.arcsin((x[2*k+1])/(new_x[k]))
                    else:
                        angles[k] = 2*np.pi-2*np.arcsin((x[2*k+1])/(new_x[k]))
                else:
                    angles[k] = 0

            angles = np.concatenate((inner_angles,angles))
        return angles
    
    def apply_gate(qc, num_qubits, value):
        """ This function add the N-control Ry gate given a 
            quantum circuit.
            input:
                qc : QuantumCircuit 
                num_qubits: which qubits are gona be affected.
                value : float = value for the Ry gate.
        """
        if num_qubits == 0:
            qc.ry(value, 0) 
        else:
            c3h_gate = RYGate(value).control(num_qubits-1)
            qc.append(c3h_gate, list(np.arange(0,num_qubits)))

    def state_preparation(prob, if_measure):

        qc = QuantumCircuit(math.log2(len(prob)), math.log2(len(prob)))
        prob = prob / np.linalg.norm(prob)
        state = np.sqrt(prob)
        angles = State_Preparation.gen_angles(state)

        ### Add quantum gates to the circuit.

        State_Preparation.apply_gate(qc, 0, angles[0])
        qc.barrier() # barrier for better visualization.

        for val in range(2, len(angles)+1):
            num_qubits_required = math.ceil(math.log2(val+1)) if val != 0 else 1
            binary_val = format(val, f'0{num_qubits_required}b')[::-1]

            binary_val = binary_val[0:num_qubits_required-1][::-1]

            for k, bit in enumerate(binary_val):
                if bit == '0':
                    qc.x(k)
            
            State_Preparation.apply_gate(qc, num_qubits_required, angles[val-1])

            for k, bit in enumerate(binary_val):
                if bit == '0':
                    qc.x(k)

            qc.barrier()

        if if_measure == 1:
            measure_qubits = np.arange(int(math.log2(len(prob))))
            qc.measure(measure_qubits, measure_qubits[::-1])

        return qc

