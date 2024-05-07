from pennylane import numpy as np
from pennylane import qchem
import re

class geometrization:

    def separar_letras_y_numeros(cadena):
        letras = re.findall('[A-Za-z]+', cadena)
        numeros = re.findall('\d+', cadena)
        return letras, numeros

    def combinar_letras_numeros(letras, numeros, longitud):
        resultado = ['I'] * longitud
        for letra, numero in zip(letras, numeros):
            posicion = int(numero)
            resultado[posicion] = letra
        return ''.join(resultado)

    def separar_constantes_y_listas(s):
        constantes = re.findall(r'\(([^)]+)\)', s)
        listas = re.findall(r'\[([^\]]+)\]', s)
        return constantes, listas

    def convertir_a_float(lista):
        lista_float = [float(valor) for valor in lista]
        return lista_float

    def crear_diccionario(lista_claves, lista_valores):
        diccionario = dict(zip(lista_claves, lista_valores))
        return diccionario

    def filtrar_por_tamano(diccionario, tamaño):
        diccionario_filtrado = {k: v for k, v in diccionario.items() if k != 'I'*tamaño}
        return diccionario_filtrado
    
    def give_hamiltonian(symbols, coordinates, basis):
        H, qubits = qchem.molecular_hamiltonian(symbols, coordinates, method = "dhf", basis=basis)
        #Ham = str(H.simplify())
        Ham = str(H)

        opts_opt = []
        opts_pos = []
        pauli_str = []

        coeffs, opts = geometrization.separar_constantes_y_listas(Ham)
        coeffs_values = geometrization.convertir_a_float(coeffs)

        for i in opts:
            opts_opt.append(geometrization.separar_letras_y_numeros(i)[0])
            opts_pos.append(geometrization.separar_letras_y_numeros(i)[1])

        for i in range(0,len(opts_opt)):
            pauli_str.append(geometrization.combinar_letras_numeros(opts_opt[i], opts_pos[i], qubits))

        pauli = geometrization.crear_diccionario(pauli_str, coeffs_values)
        #pauli_fil = geometrization.filtrar_por_tamano(pauli, qubits)

        return pauli