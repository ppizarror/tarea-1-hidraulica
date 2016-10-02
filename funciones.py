# coding=utf-8
"""
Funciones extras para calcular necesidades.
"""

# Importación de librerías
import math
import matplotlib.pyplot as plt


def get_diametern(n, dmax, dmin):
    """
    Calcula el diámetro para satisfacer un largo n
    :param n: largo a cubrir
    :param dmax: diámetro maximo
    :param dmin: diámetro mínimo
    :return:
    """
    j = 1.0
    soluc = []
    while True:
        if j == n:
            break
        d = round(n / j, 1)
        e = [d, int(j)]
        if dmin <= d <= dmax:
            if e not in soluc:
                soluc.append(e)
        j += 1
    return soluc


def get_final_d_solution(a, b):
    """
    Intercepta dos listas a y b y retorna la solución final

    :param a: lista a
    :param b: lista b
    :return:
    """
    sol = []  # soluciones
    for j in range(0, len(a)):
        for k in range(0, len(b)):
            if a[j][0] == b[k][0]:
                sol.append([a[j][0], a[j][1], 2 * b[k][1] - 1])
    return sol


def get_cant_tuberia(lg, diam, k, l):
    """
    Retorna la cantidad de tuberías
    :param lg:
    :param diam:
    :param k:
    :param l:
    :return:
    """
    return [round(diam * l * (k - 0.5), 1), round(lg + diam / 2 * (l - 1), 1)]


def get_cant_tuberia_from_d(d, pos, largo):
    """
    Retorna la cant de tub desde arreglo d con pos
    :param d: Arreglo
    :param pos: posición
    :param largo: distancia de sistema a rio
    :return:
    """
    return get_cant_tuberia(largo, d[pos][0], d[pos][1], d[pos][2])


def get_area_residual(n, m, diam, k, l):
    """
    Calcula el area residual de un rectángulo de nxm con nxl círculos de
    radio d
    :param n: alto
    :param m: ancho
    :param diam: diámetro
    :param k: cantidad en n
    :param l: cantidad en m
    :return:
    """
    af = n * m
    ad = math.pi * math.pow(diam / 2, 2) * k * l
    aff = (math.pow(diam, 2) * (1 - math.pi / 4)) / (af - ad)
    return [af - ad, round((af - ad) / af, 2), round(aff, 3) * 1000]


def get_consumo_caudal_regadio(c, d):
    """
    Calcula el consumo en m3/s de un regadero
    :param c:
    :param d:
    :return:
    """
    return c * math.pow(d, 2)


def get_consumo_con_minimo_regadero(qhora, prop_regadero):
    """
    Retorna la cantidad de horas que debe funcionar
    :param qhora:
    :param prop_regadero:
    :return:
    """
    return [round(qhora * 24 / prop_regadero[0], 4),
            round(qhora * 24 / prop_regadero[1], 4)]


def add_coma(snum):
    """
    Añade comas como sumas
    :param snum:
    :return:
    """
    s = str(float(snum))
    i = s.index('.')  # Se busca la posición del punto decimal
    while i > 3:
        i -= 3
        s = s[:i] + ',' + s[i:]
    s = s.replace('.', '-').replace(',', '.').replace('-', ',')
    s = s.replace(',0', '')
    return s


# noinspection SpellCheckingInspection
def get_precios_regaderos(diametro):
    """
    Retorna el precio por cada diámetro
    :param diametro:
    :return:
    """
    r = diametro / 2
    if 10 <= r <= 12:
        return 15017
    elif 12 < r <= 13:
        return 14586
    elif 15 <= r <= 17:
        return 14338
    elif 18 <= r <= 26:
        return 51227
    else:
        raise Exception('Radio no se conoce')


def calculo_reynolds(q, w):
    """
    Calcula el reynolds con un caudal q y diámetro tubería w
    :param q:
    :param w:
    :return:
    """
    return (4 * q) / (math.pi * math.pow(10, -6) * w)


def calcular_radio(l):
    """
    Calcula el radio en función de su distancia
    :param l:
    :return:
    """
    return round((2 * l) / math.pi, 3)


def function_fc_coef_curva(re, w, r):
    """
    Calculo fc parámetro coef curva
    :param re:
    :param w:
    :param r:
    :return:
    """
    return 0.336 / pow(re * pow(w / (2 * r), 0.5), 0.2)


def function_alpha_coef_curva(r, d):
    """
    Calculo alpha coef curvatura
    :param r:
    :param d:
    :return:
    """
    if float(r) / d < 9.85:
        return 0.95 + 4.42 * pow(d / r, 1.96)
    else:
        return 1


def calcular_coef_curva(q, w, r, ang=90):
    """
    Calcula el coef de curvatura
    :param q:
    :param w:
    :param r:
    :param ang:
    :return:
    """
    q = float(q)
    w = float(w)
    r = float(r)
    re = calculo_reynolds(q, w)
    fc = function_fc_coef_curva(re, w, r)
    alp = function_alpha_coef_curva(r, w)
    dr = pow(w / r, 2)
    if 0 < re * dr <= 360:
        return 0.0175 * alp * fc * ang * (r / w)
    else:
        return 0.00431 * alp * ang * pow(re, -0.17) * pow(r / w, 0.84)


def alt_vel(q, w):
    """
    Retorna la altura de velocidad asociada al caudal q que pasa en un
    diámetro w

    :param q: Caudal.
    :param w: Diámetro.

    :return: Altura de velocidad en metros
    """
    return (8 * pow(q, 2)) / (9.8 * math.pow(math.pi, 2) * math.pow(w, 4))


def calculate_friction(e, d):
    """
    Calcula la fricción a partir del espesor y el diámetro
    :param e:
    :param d:
    :return:
    """
    return 0.25 / math.pow(math.log10(float(d) / e) + 0.56820172, 2)


def calc_k_derivac(q, qo, qsigue=True):
    """
    Calcula el factor de la derivación.
    Qo -> Q1
       |
       Q2

    :param q: Q que sigue por la tubería
    :param qo: Q antes de la derivación
    :param qsigue: Indicia si q es el que sigue en la tubería tras Qo
    :return: Factor de pérdida
    """
    f = float(q) / qo
    if qsigue:
        if 0 <= f <= 0.2:
            return 0.4 + 0.05 * f / 0.2
        elif 0.2 < f <= 0.4:
            return 0.45 + (0.2 - 0.45) * (f - 0.2) / 0.2
        elif 0.4 < f <= 0.6:
            return 0.2 + (0.1 - 0.2) * (f - 0.4) / 0.2
        elif 0.6 < f <= 0.8:
            return 0.1 + (0.05 - 0.1) * (f - 0.6) / 0.2
        else:
            return 0.05
    else:
        if 0 <= f <= 0.2:
            return 1.3 + (1.1 - 1.3) * f / 0.2
        elif 0.2 < f <= 0.4:
            return 1.1 + (0.96 - 1.1) * (f - 0.2) / 0.2
        elif 0.4 < f <= 0.6:
            return 0.96 + (0.9 - 0.96) * (f - 0.4) / 0.2
        elif 0.6 < f <= 0.8:
            return 0.9 + (0.88 - 0.9) * (f - 0.6) / 0.2
        else:
            return 0.88 + (0.96 - 0.08) * (f - 0.8) / 0.2


def perdida_contracc(wg, wp):
    """
    Coeficiente de pérdida por contracción de la tubería
    :param wg: Diámetro grande
    :param wp: Diámetro pequeño
    :return:
    """
    return math.pow(math.pow(wg, 2) / math.pow(wp, 2) - 1, 2)


def calculate_b(pv, e, f, d, w, qe, q, pc, lar, l, zc, m, pent=0.44):
    """
    Calcula la altura de agua de la bomba B.

    :param pv: Presión de vapor
    :param e: Parámetro de error asociado a presión de vapor
    :param f: fricción en tubería
    :param d: Diámetro de riego (diámetro de alcance)
    :param w: Diámetro de tubería
    :param qe: Caudal de entrada
    :param q: Caudal de salida por cada rama
    :param pc: Perdidas de codo
    :param lar: Largo de tubería antes de sistema
    :param l: Cantidad de ramas
    :param zc: altura del rio
    :param m: Largo de la tubería gruesa
    :param pent: Perdida entrada
    :return:
    """

    # Sumatoria por perdidas en friccion
    fper = 0.0
    sf = f * float(m - d) / (l * w)  # Perdida por friccion
    for i in range(1, l):
        qit = qe - i * q  # Caudal en cada tramo del tubo por friccion
        if qit < 0:
            break
        sder = calc_k_derivac(qit, qe + q * (1 - i))  # Derivación
        fper += (sf + sder) * alt_vel(qit, w)

    fper_prev = pc + pent + lar * f / w  # Factor de perdida para tubería L
    b = -zc + pv * (1 + e) + fper + fper_prev * alt_vel(qe, w)
    return b


# noinspection SpellCheckingInspection
def calculate_min_b(pv, e, f, d, w, wp, qe, q, pc, lar, l, k, zc, m, mp, b,
                    kreg, kvalv, nums, etq, pent=0.44):
    """
    Calcula la altura de agua de la bomba B.

    :param pv: Presión de vapor
    :param e: Parámetro de error asociado a presión de vapor
    :param f: friccion en tubería
    :param d: Diámetro de riego (diámetro de alcance)
    :param w: Diámetro de tubería
    :param wp: Diámetro de tubería pequeña
    :param qe: Caudal de entrada
    :param q: Caudal de salida por cada rama
    :param pc: Perdidas de codo
    :param lar: Largo de tubería antes de sistema
    :param l: Cantidad de ramas
    :param k: Cantidad de regaderos en cada rama
    :param zc: altura del rio
    :param m: Largo de la tubería gruesa
    :param mp: Largo de la tubería pequeña
    :param b: Bomba instalada
    :param kreg: Coeficiente de pérdida de los regaderos
    :param kvalv: Coeficiente de pérdida en las válvulas
    :param nums: Numero de la solucion
    :param etq: Etiqueta a la imagen guardada
    :param pent: Perdida entrada
    :return:
    """

    # Se ejecuta para cada una de las cañerías pequeñas
    b_min = []

    # Gráficos
    contrib_fricc_tub = []
    contrib_fricc_tub_rama = []
    contrib_bprev = []

    # Se calcula el bernoulli antes de que empiecen las tuberías pequeñas
    fper_prev = pc + pent + lar * f / w  # Factor de perdida para tubería L
    b_prev = zc + b - fper_prev * alt_vel(qe, w) - 2 * pv * (1 + e)

    # Perdida por friccion en tubería grande
    sf = f * float(m - d) / (l * w)
    sfp = f * float(mp - d / 2) / (k * wp)

    # Se calcula la pérdida en cada rama
    per_rama = 0.0
    q_regadero = float(q) / k

    # Se añade pérdida por fricción, derivación y regadero
    for j in range(1, k):
        qit = q - j * q_regadero  # Caudal en cada tramo del tubo por friccion
        qpder = calc_k_derivac(qit, qit + q_regadero)
        per_rama += (sfp + qpder) * alt_vel(qit, wp) + kreg * alt_vel(q, wp)

    # Se calcula la bomba mínima en cada rama
    for v in range(1, l + 1):

        prama_i = per_rama

        # Se añade la derivación a la tubería pequeña
        prama_i += calc_k_derivac(q, qe + q * (1 - v), False) * alt_vel(q, wp)
        prama_i += (perdida_contracc(w, wp) + kvalv) * alt_vel(
            qe + q * (1 - v), wp)

        k_tub_per = 0.0
        # Se calcula la pérdida en la tubería grande hasta llegar a esa rama
        for i in range(1, v):
            qit = qe - i * q  # Caudal en cada tramo del tubo por friccion
            if qit < 0:
                break
            # Derivación
            sder = calc_k_derivac(qit, qe + q * (1 - i))
            k_tub_per += (sf + sder) * alt_vel(qit, w)

        b_min_ap = max(k_tub_per + prama_i - b_prev, 0)
        cft = max(k_tub_per, 0)
        cftr = max(k_tub_per + prama_i, 0)
        contrib_fricc_tub.append(cft)
        contrib_fricc_tub_rama.append(cftr)
        contrib_bprev.append(b_prev)
        b_min.append(b_min_ap)

    # Se grafica la bomba vs rama
    fig = plt.figure()
    plt.xlabel('Numero de rama')
    plt.ylabel('Altura minima de cada bomba [m]')
    plt.title('Variacion altura minima por cada rama con Qe={0}m'.format(qe))
    plt.grid(True)
    plt.plot(range(1, l + 1), b_min, '-b', label='Altura bomba')
    plt.legend(loc=4)
    plt.savefig('solucion {0}/{1}_var_alt_minima_bomba.png'.format(nums, etq),
                dpi=300)
    plt.close(fig)

    # Se grafican las contrib
    fig = plt.figure()
    plt.xlabel('Numero de rama')
    plt.ylabel('Altura minima de cada bomba [m]')
    plt.title('Contribucion de las perdidas en cada rama con Qe={0}m'.format(
        qe))
    plt.grid(True)
    plt.plot(range(1, l + 1), contrib_fricc_tub, '-b', label='Friccion tubo '
                                                             'grande')
    plt.plot(range(1, l + 1), contrib_fricc_tub_rama, '-r',
             label='Friccion tubo grande y pequeno')
    plt.plot(range(1, l + 1), contrib_bprev, '-c',
             label='Bernoulli previo a las ramas')
    plt.legend(loc=4)
    plt.savefig('solucion {0}/{1}_var_alt_perdidas_minima_bomba.png'.format(
        nums, etq), dpi=300)
    plt.close(fig)

    return max(b_min)
