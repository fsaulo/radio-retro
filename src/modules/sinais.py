#!/usr/bin/env python3

'''
Ferramentas para analise de sinais.

Escrito por Saulo G. Felix
Licença BSD ou parecida.
'''

import numpy as np
import matplotlib.pyplot as plt
import fourier

def specgram(data, fa=None):
    janela = round(20e-3 * len(data))
    avanco = round(0.8*janela)
    ktmax = round((len(data)-janela)/(avanco))
    kfmax = janela

    try:
        from tqdm import tqdm
        S = specmat(data, ktmax, kfmax, avanco, janela, module=tqdm)
    except ModuleNotFoundError:
        S = specmat(data, ktmax, kfmax, avanco, janela)

    half = round(kfmax/2)
    S = (S.T[:half])/np.max(S)

    if fa is None:
        tmax = ktmax/janela
        fmax = round(kfmax/2)
    else:
        tmax = len(data)/fa
        fmax = fa/2

    from matrizes import matgraph
    matgraph(S, colorbar=False, invcolor=True, origin='lower', xlabel='Tempo (s)',
             ylabel='Frequência (Hz)', extent=(0, tmax, 0, fmax))

def specmat(data, ktmax, kfmax, avanco, janela, module=None):
    S = np.ones((ktmax, kfmax))
    if module is None:
        for k in range(0, ktmax):
            p = avanco*k
            X = fourier.dft(data[p:p+janela])
            S[k:k+1] = abs(X.T)
    else:
        for k in module(range(0, ktmax)):
            p = avanco*k
            X = fourier.dft(data[p:p+janela])
            S[k:k+1] = abs(X.T)

    return S

def fir(x, a, b, c=1):
    return np.abs(( 1 + a * (x ** 2) + b  * (x) + c ))

if __name__== '__main__':
    fa = 4400
    t = np.arange(0, 2, 1/fa)
    s = np.cos(2*np.pi*250*t)*np.heaviside(-(t-0.5), 1) + \
    np.cos(2*np.pi*100*t)*np.heaviside(t-0.5, 1) + \
    np.cos(2*np.pi*600*t)*np.heaviside(t-1, 1)

    specgram(s, fa)
