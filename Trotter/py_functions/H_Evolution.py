import numpy as np
from qiskit import QuantumCircuit

class H_Evolution:

    def parity(array):
        resultados = []
        indice_anterior = None
        for i, num in enumerate(array[0]):
            if num == '1':
                if indice_anterior is not None:
                    resultados.append([indice_anterior, i])
                indice_anterior = i
        return resultados

    def convertir_array(array):
        nuevo_array = ['1' if char != 'I' else '0' for char in array[0]]
        return [nuevo_array]

    def encontrar_ultimo_uno(array):
        posicion_ultimo_uno = None

        for i in range(len(array[0])-1, -1, -1):
            if array[0][i] == '1':
                posicion_ultimo_uno = i
                break 
        return posicion_ultimo_uno
    
    def exp_h(pauli, prob, t, n):

        list_opt = list(pauli.keys())
        dim_opt = len(list_opt[0])

        qc = QuantumCircuit(dim_opt)

        pos = 0

        for i in range(0, len(prob)):
            if prob[i] != 0.0 or prob[i] != 0j:

                #############################
                array_unos = H_Evolution.convertir_array([list_opt[i]])

                contador_uno = 0

                for sublista in array_unos:
                    for elemento in sublista:
                        if elemento == '1':
                            contador_uno += 1
                
                if contador_uno == 1:
                    for k in list_opt[i]:
                        if k == 'Z':
                            qc.rz((prob[i]*2*t)/n, H_Evolution.encontrar_ultimo_uno(array_unos))
                        elif k == 'X':
                            qc.rx((prob[i]*2*t)/n, H_Evolution.encontrar_ultimo_uno(array_unos))
                        elif k == 'Y':
                            qc.ry((prob[i]*2*t)/n, H_Evolution.encontrar_ultimo_uno(array_unos))
                    
                #############################
                else:

                    for j in list_opt[i]:
                        if j == 'X':
                            qc.ry(np.pi/2, pos)
                        elif j == 'Y':
                            qc.rx(np.pi/2, pos)
                        pos = pos + 1 

                    pos = 0

                    array_unos = H_Evolution.convertir_array([list_opt[i]])
                    array_cnots = H_Evolution.parity(array_unos)

                    for cnot_iter in array_cnots:
                        qc.cnot(cnot_iter[0], cnot_iter[1])

                    qc.rz((prob[i]*2*t)/n, H_Evolution.encontrar_ultimo_uno(array_unos))

                    for cnot_iter in reversed(array_cnots):
                        qc.cnot(cnot_iter[0], cnot_iter[1])

                    for j in list_opt[i]:
                        if j == 'X':
                            qc.ry(-np.pi/2, pos)
                        elif j == 'Y':
                            qc.rx(-np.pi/2, pos)
                        pos = pos + 1 

                    pos = 0

        return qc
    
    def Exp_evolution(pauli, prob, t, n):

        list_opt = list(pauli.keys())
        dim_opt = len(list_opt[0])

        qc = QuantumCircuit(dim_opt)

        ### Exponential circuit
        exp = H_Evolution.exp_h(pauli, prob, t, n)
        qc_exp = QuantumCircuit(dim_opt)
        qc_exp.append(exp, list(np.arange(0,dim_opt)))
    
        ### Repetition circuit.
        for i in np.arange(n):
            qc.append(qc_exp, list(np.arange(0,dim_opt)))

        return qc
