import numpy as np
from itertools import product

class pauli_composition:

    def Decomposition(A):

        Pauli_Matrices = ['I', 'X', 'Y', 'Z']
        Tras = []
        dim = int(np.log2(len(A)))

        I = np.array([[1,0],[0,1]])
        X = np.array([[0,1],[1,0]])
        Y = np.array([[0, -1j],[1j, 0]])
        Z = np.array([[1,0],[0,-1]])

        Permutations = []
        for i in product(Pauli_Matrices, repeat = dim):
            Permutations.append(i)

        Matrices = Permutations.copy()

        for j in range(len(Matrices)):
            Res = 1
            for i in range(len(Matrices[0])):
                if Matrices[j][i] == 'I':
                    Res = np.kron(I,Res)
                elif Matrices[j][i] == 'X':
                    Res = np.kron(X,Res)
                elif Matrices[j][i] == 'Y':
                    Res = np.kron(Y,Res)
                else:
                    Res = np.kron(Z,Res)
            Tras.append(Res)

        coefficiens = []

        for i in range(len(Tras)):
            coefficiens.append((1/2**dim)*np.trace(np.dot(Tras[i],A)))

        Decomposition_List = {''.join(Permutations[i]): coefficiens[i] for i in range(len(Permutations))}

        Decomposition_List['I'*dim] = 0.0

        return Decomposition_List