#!/usr/bin python3

'''
Visualizacao de matrizes 2-d

Escrito por Saulo G. Felix
Licença BSD ou parecida.
'''

import numpy as np
import matplotlib.pyplot as plt

from matplotlib import colors

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

def print_matrix(mat):
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in mat]))
