'''
Ferramentas para analise de sinais.

Escrito por Saulo G. Felix
Licença BSD ou parecida.
'''

import numpy as np
import fourier
import matplotlib.pyplot as plt
from matplotlib import colors

def specgram(data, fa=44100, period=20e-3, windowing=0.8):
    """ Computes the spectrogram using the Short-time Fourier Transform

    ----------
    Beware that this implementation of the short-time Fourier Transform
    doesn't use the Fast Fourier Transform algorithm thus takes much more time
    than the others mostly commonly used implementations.
    This was not conceived to be the faster nor accurate spectrogram
    implementation, its real purpose is to verify the results learnt in class,
    therefore the results presented may not be correct. Use it with caution.

    ----------
    Parameters
    data: One-dimensional array
    fa: Frequency sampling rate
    timing: Period of time between each computation of the FT in seconds
    windowing: A floating point that represents the percentage of the width of
        the chosen short-time window that will be overlaped measured in samples

    """

    janela = round(period * len(data))
    avanco = round(windowing*janela)
    ktmax = round((len(data)-janela)/(avanco))
    kfmax = janela

    try:
        from tqdm import tqdm
        S = specmat(data, ktmax, kfmax, avanco, janela, module=tqdm)
    except ModuleNotFoundError:
        S = specmat(data, ktmax, kfmax, avanco, janela, module=None)

    half = round(kfmax/2)
    S = (S.T[:half])/np.max(S)

    if fa is None:
        tmax = ktmax/janela
        fmax = round(kfmax/2)
    else:
        tmax = len(data)/fa
        fmax = fa/2

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

def matgraph(mat, colorbar=True, invcolor=False, origin=None, aspect='auto',
             xlabel=None, ylabel=None, extent=None):

    mat = np.matrix(mat if not invcolor else -mat)
    width, height = mat.shape
    data = np.floor(mat*255)+1
    v = np.linspace(0, 1, 256)
    cores = v[:, None] * np.ones((1,3))
    cmap = colors.ListedColormap(cores)
    img = plt.imshow(data, cmap=cmap, origin=origin, aspect=aspect, extent=extent)

    if colorbar is True:
        plt.colorbar(img, cmap=cmap)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def alma(h, fa, pieces=500):
    w = np.linspace(0, np.pi, pieces)
    H = np.zeros(len(w)) * 1j
    for k in range(0, len(w)):
        for i in range(0, len(h)):
            H[k] += h[i]*np.exp(-1j*w[k]*i)
        print('current: {} remainder: {}'.format(k, len(w) - k), end='\r')
    return np.array(H)

def lowpass(x, fa, bandwidth=500, N=200):
    n = np.arange(-round(N/2), round(N/2))
    h = np.sinc(2*bandwidth*n/fa)
    y = np.zeros(len(x))
    for n in range(0, len(x)):
        y[n] = sum([x[n - k] * h[k] for k in range(0, N)])
        print('current: {} remainder: {}'.format(n, len(x) - n), end='\r')
    return y

def convolve(x1, x2):
    y = np.zeros(len(x))
    for n in range(0, len(x1)):
        y[n] = sum([x1[n - k] * x2[k] for k in range(0, x2)])
    return y

def bandpass(x, fa, f0, bandwidth=500, N=300):
    n = np.arange(-round(N/2), round(N/2))
    h = np.sinc(2*bandwidth/fa*n) * blackman_window(fa, N)
    m = np.arange(0, N)
    m0 = np.cos(2*np.pi*f0*m/fa)
    return np.convolve(x, h*m0)

def blackman_window(fa, N):
    n = np.arange(0, N)
    return 0.42 - 0.5*np.cos(2*np.pi*n/(N-1)) + 0.08*np.cos(4*np.pi*n/(N-1))

def rms(x):
    return np.sqrt(np.mean(x**2))
    
if __name__== '__main__':
    fa = 4400
    t = np.arange(0, 2, 1/fa)
    s = np.cos(2*np.pi*250*t)*np.heaviside(-(t-0.5), 1) + \
    np.cos(2*np.pi*100*t*t*t)*np.heaviside(t-0.5, 1) + \
    np.cos(2*np.pi*600*t)*np.heaviside(t-1, 1)
    S = specgram(s, fa, 20e-3,0.1)
