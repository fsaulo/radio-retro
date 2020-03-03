'''
PDS por analises de Fourier.

Escrito por Saulo G. Felix
Licença BSD ou parecida.
'''

import numpy as np

def index2d(mat):
    try:
        return mat.shape
        raise ValueError('Apenas matriz 2-d')
    except Exception:
        pass

def matdft(dim=1):
    mat = np.matrix([[np.exp(-1j*2*np.pi*i*k/dim) for i in range(dim)] for k in range(dim)])
    return mat

def dft2d(mat):
    mat = np.matrix(mat)
    [M, N] = index2d(mat)
    U = matdft(M)
    V = U if M == N else matdft(N)
    xx = (U * mat) * V.conj().T
    return xx

def idft2d(mat):
    mat = np.matrix(mat)
    [M, N] = index2d(mat)
    U = matdft(M)
    V = U if M == N else matdft(N)
    xx = 1/(M*N) * U.H (mat * V)
    return xx

def dft(vet):
    L = len(vet)
    vet = np.array([vet])
    U = matdft(L)
    xx = np.array(U * vet.T)
    return xx

def idft(vet):
    L = len(vet)
    vet = np.array(vet)
    U = matdft(L)
    xx = (1/L) * np.array(U.H * vet)
    return xx

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    tf = 2
    fa = 30
    N = tf*fa
    t = np.arange(0, tf, 1/fa)
    y = .7*np.sin(2*np.pi*t*4) + .4*np.cos(2*np.pi*t*12)
    w = [n*fa/N for n in range(0, N)]
    Y = dft(y)
    espectro = abs(Y)
    plt.plot(w, espectro, lw=2)
    plt.xticks(np.arange(0, fa, 2))
    plt.show()
