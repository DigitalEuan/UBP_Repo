'''
Universal Binary Principle (UBP) Error Correction Module

This module provides full implementations for the error correction codes
used in the UBP framework, including Hamming, BCH, and a manual implementation
of the Golay code.

Author: Euan Craig, New Zealand
Date: 7 October 2025
'''

import numpy as np
import galois
from . import constants as const

# --- Golay Code G(23,12) Manual Implementation ---

class Golay:
    def __init__(self, tipo=23):
        self.I12= [[1,0,0,0,0,0,0,0,0,0,0,0],
                [0,1,0,0,0,0,0,0,0,0,0,0],
                [0,0,1,0,0,0,0,0,0,0,0,0],
                [0,0,0,1,0,0,0,0,0,0,0,0],
                [0,0,0,0,1,0,0,0,0,0,0,0],
                [0,0,0,0,0,1,0,0,0,0,0,0],
                [0,0,0,0,0,0,1,0,0,0,0,0],
                [0,0,0,0,0,0,0,1,0,0,0,0],
                [0,0,0,0,0,0,0,0,1,0,0,0],
                [0,0,0,0,0,0,0,0,0,1,0,0],
                [0,0,0,0,0,0,0,0,0,0,1,0],
                [0,0,0,0,0,0,0,0,0,0,0,1]]

        self.A = [[0,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,0,1,1,1,0,0,0,1,0],
                [1,1,0,1,1,1,0,0,0,1,0,1],
                [1,0,1,1,1,0,0,0,1,0,1,1],
                [1,1,1,1,0,0,0,1,0,1,1,0],
                [1,1,1,0,0,0,1,0,1,1,0,1],
                [1,1,0,0,0,1,0,1,1,0,1,1],
                [1,0,0,0,1,0,1,1,0,1,1,1],
                [1,0,0,1,0,1,1,0,1,1,1,0],
                [1,0,1,0,1,1,0,1,1,1,0,0],
                [1,1,0,1,1,0,1,1,1,0,0,0],
                [1,0,1,1,0,1,1,1,0,0,0,1]]
    
        self.A_prima = [[0,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,0,1,1,1,0,0,0,1],
                        [1,1,0,1,1,1,0,0,0,1,0],
                        [1,0,1,1,1,0,0,0,1,0,1],
                        [1,1,1,1,0,0,0,1,0,1,1],
                        [1,1,1,0,0,0,1,0,1,1,0],
                        [1,1,0,0,0,1,0,1,1,0,1],
                        [1,0,0,0,1,0,1,1,0,1,1],
                        [1,0,0,1,0,1,1,0,1,1,1],
                        [1,0,1,0,1,1,0,1,1,1,0],
                        [1,1,0,1,1,0,1,1,1,0,0],
                        [1,0,1,1,0,1,1,1,0,0,0]]

        self.n = 12
        self.p = 2
        self.tipo = tipo
     
        if not(self.tipo in [24,23]):
            return ValueError('El tipo de Golay seleccionado ('+self.tipo+') no es un tipo válido.')
        
        self.G24 = self.concatenar(self.I12,self.A)
        self.G23 = self.concatenar(self.I12,self.A_prima)

    def get_columna(self,matriz, n):
        A_col = [[0] * len(matriz[0])]
        for k in range(len(self.A[0])):
            A_col[0][k] = self.A[n][k]
        return A_col
    
    def eliminar_columna(self, matriz, col):
        return [list(x) for x in zip(*[d for i,d in enumerate(zip(*matriz)) if not i == col])]

    def sumar(self,A,B):
        long = len(A[0])
        C = [[0]*long]
        for index in range(long):
            C[0][index] = A[0][index] ^ B[0][index]
        return C
    
    def multiplicar(self, A, B):
        filas = len(A)
        columnas = len(B[0])
        C = [[0 for k in range(columnas)] for i in range(filas)]
        for i in range(filas):
            for j in range(columnas):
                for k in range(len(B)):
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % self.p
        return C

    def transpuesta(self,matriz):
        filas = len(matriz[0])
        columnas = len(matriz)
        transpuesta = [[0 for k in range(columnas)] for i in range(filas)]
        for i in range(filas):
            for j in range(columnas):
                transpuesta[i][j] = matriz[j][i]
        return transpuesta

    def concatenar(self,A,B):
        num_filas = len(A)
        toret = [0] * num_filas
        for fila in range(num_filas):
            toret[fila] = A[fila] + B[fila]
        return toret
    
    def aplanar(self,vector):
        return ''.join([str(j) for j in vector[0]])

    def rellenar(self,datos):
        prefijo, relleno = '',''
        tamano = len(datos)
        resto = tamano % self.n
        if resto != 0:
            tamano_relleno = self.n - resto
            prefijo = '{0:012b}'.format(tamano_relleno)
            relleno = '1' * tamano_relleno
        return prefijo + datos + relleno
    
    def get_vector(self,palabra):
        vector = [[]]
        for char in palabra:
            vector[0].append(int(char))
        return vector
    
    def anadir_peso_impar(self, r):
        peso = r.count('1')
        r+=str((peso+1)%self.p)
        return r
    
    def encode(self, datos):
        datos = self.rellenar(datos)
        codificado_list = []
        for i in range(0,len(datos),self.n):
            palabra = datos[i:i+self.n]
            vector = self.get_vector(palabra)
            if(self.tipo == 24):
                c = self.multiplicar(vector,self.G24)
            elif(self.tipo == 23):
                c = self.multiplicar(vector,self.G23)
            for bit in c[0]:
                codificado_list.append(bit)
        return codificado_list
    
    def algoritmo_decodificacion(self, r):
        error = None
        vector_r = self.get_vector(r)
        Gt = self.transpuesta(self.G24)
        s = self.multiplicar(vector_r,Gt)
        w_s = sum(s[0])
        if w_s <= 3:
            error = [s[0] + [0] * 12]
        else:
            for j in range(12):
                sum_vec = self.sumar(s,self.get_columna(self.A,j))
                peso_sum = sum(sum_vec[0])
                if peso_sum <= 2:
                    error = [sum_vec[0] + self.I12[j]]
                    break
            if error == None:
                sA = self.multiplicar(s, self.transpuesta(self.A))
                w_sA = sum(sA[0])
                if w_sA <= 3:
                    error = [[0] * 12 + sA[0]]
                for j in range(12):
                    sum_vec = self.sumar(sA,self.get_columna(self.A,j))
                    peso_sum = sum(sum_vec[0])
                    if peso_sum <= 2:
                        error = [self.I12[j] + sum_vec[0]]
                        break
        if error == None:
            raise Exception("No se ha podido decodificar la palabra "+r+". Error al menos triple")
        else:
            return self.sumar(vector_r,error)

    def decode(self, datos):
        if(self.tipo == 24):
            u = self.decode24(datos)
        elif(self.tipo == 23):
            u = self.decode23(datos)
        prefijo = u[:12]
        u = u[12:-int(prefijo,2)]
        return u
    
    def decode24(self, datos):
        resultado = ''
        for i in range(0,len(datos),24):
            r = datos[i:i+24]
            try:
                resultado += self.aplanar(self.algoritmo_decodificacion(r))[:12]
            except Exception as e:
                resultado += str(0) * 12
                print(e)
        return resultado

    def decode23(self, datos):
        resultado = ''
        for i in range(0,len(datos),23):
            r = datos[i:i+23]
            try:
                ri = self.anadir_peso_impar(r)
                c_prima = self.aplanar(self.algoritmo_decodificacion(ri))
                c_prima = c_prima[:-1]
                resultado += c_prima[:12]
            except Exception as e:
                resultado += str(0) * 12
                print(e)
        return resultado

# --- BCH and Hamming Codes using `galois` ---

BCH = galois.BCH(n=const.BCH_PARAMS["n"], k=const.BCH_PARAMS["k"])
HAMMING = galois.BCH(n=7, k=4) # Hamming(7,4) is a BCH code with t=1

def encode_bch(data):
    return BCH.encode(data)

def decode_bch(encoded_data):
    return BCH.decode(encoded_data)

def encode_hamming(data):
    return HAMMING.encode(data)

def decode_hamming(encoded_data):
    return HAMMING.decode(encoded_data)

if __name__ == "__main__":
    print("Testing UBP Error Correction Module...")

    # Test Golay
    golay = Golay(tipo=23)
    data_golay = "110100101101"
    encoded_golay = golay.encode(data_golay)
    encoded_str = "".join(map(str, encoded_golay))
    error_pos = 5
    encoded_with_error = list(encoded_str)
    encoded_with_error[error_pos] = '1' if encoded_with_error[error_pos] == '0' else '0'
    encoded_with_error = "".join(encoded_with_error)

    decoded_golay = golay.decode(encoded_with_error)
    print(f"Original Golay data: {data_golay}")
    print(f"Encoded Golay data:  {encoded_str}")
    print(f"Encoded with error:  {encoded_with_error}")
    print(f"Decoded Golay data:  {decoded_golay}")
    print(f"Golay Correct: {data_golay == decoded_golay}")

    # Test BCH
    data_bch = galois.GF(2).Random(BCH.k)
    encoded_bch = encode_bch(data_bch)
    decoded_bch = decode_bch(encoded_bch)
    print(f"BCH Correct: {np.array_equal(data_bch, decoded_bch)}")

    # Test Hamming
    data_hamming = galois.GF(2).Random(HAMMING.k)
    encoded_hamming = encode_hamming(data_hamming)
    decoded_hamming = decode_hamming(encoded_hamming)
    print(f"Hamming Correct: {np.array_equal(data_hamming, decoded_hamming)}")

