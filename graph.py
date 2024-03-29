# coding=utf-8
"""
Graficar cosas
"""

# Importar librerías
import matplotlib.pyplot as plt
from const import *

# Constantes
DDX = 0.05  # Porcentaje de holgura en el ancho
DDY = 0.1  # Porcentaje de holgura en el alto


# noinspection SpellCheckingInspection
def plot_solution(d, v, nums):
    """
    Plotea la solucion
    :param v: Solucion elegida
    :param d: Diametros
    :param nums: Numero de la solución
    :return:
    """

    # Se crea el plot
    fig, ax = plt.subplots()
    plt.xlim([-DDY * M, M * (1 + DDX)])
    plt.ylim([-DDX * 3 * N, N * (1 + DDY)])

    # Se plotean los circulos
    diam = d[v][0]
    dx = diam / 2
    typecolor = -1
    for i in range(1, d[v][2] + 1):
        dy = diam / 2
        for j in range(1, d[v][1] + 1):
            if typecolor < 0:
                c = plt.Circle((dx, dy), radius=diam / 2, color='#3284D6')
                ax.add_patch(c)
            dy += diam
        typecolor *= -1
        dx += diam / 2
    typecolor = 1
    dx = diam / 2
    for i in range(1, d[v][2] + 1):
        dy = diam / 2
        for j in range(1, d[v][1] + 1):
            if typecolor < 0:
                c = plt.Circle((dx, dy), radius=diam / 2, color='#0066cc')
                ax.add_patch(c)
            dy += diam
        typecolor *= -1
        dx += diam / 2

    # Se plotean tuberías
    dx = diam / 2
    for w in range(1, d[v][2] + 1):
        plt.plot([dx, dx], [0, N - diam / 2], color='#000000', linewidth=2.0)
        dx += diam / 2
    plt.plot([0, M - diam / 2], [-0.05, -0.05], color='#000000', linewidth=5.0)
    plt.plot([0, 0], [-L, 0], color='#000000', linewidth=5.0)

    # Se rotulan gráficos
    plt.xlabel('$x$ [m]')
    plt.ylabel('$y$ [m]')
    plt.title('Esquema con $d={0}m$'.format(diam))

    plt.savefig('solucion {0}/esquema_solucion.png'.format(nums), dpi=300)
