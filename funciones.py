# coding=utf-8
"""
Funciones extras para calcular necesidades.
"""

# Importación de librerías
import math


def get_diametern(n, dmax, dmin):
    """
    Calcula el diametro para satisfacer un largo n
    :param n: largo a cubir
    :param dmax: diametro maximo
    :param dmin: diametro minimo
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
    Intersecta dos listas a y b y retorna la solución final
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
    Retorna la cantidad de tuberias
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
    :param pos: posicion
    :param largo: distancia de sistema a rio
    :return:
    """
    return get_cant_tuberia(largo, d[pos][0], d[pos][1], d[pos][2])


def get_area_residual(n, m, diam, k, l):
    """
    Calcula el area residual de un rectangulo de nxm con nxl circulos de
    radio d
    :param n: alto
    :param m: ancho
    :param diam: diametro
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


def get_precios_regaderos(diametro):
    """
    Retorna el precio por cada diametro
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
    Calcula el reynolds con un caudal q y diametro tuberia w
    :param q:
    :param w:
    :return:
    """
    return (4 * q) / (math.pi * math.pow(10, -6) * w)


def calcular_radio(l):
    """
    Calcula el radio en fucion de su distancia
    :param l:
    :return:
    """
    return round((2 * l) / math.pi, 3)


def function_fc_coef_curva(re, w, r):
    """
    Calculo fc parametro coef curva
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
    diametro w

    :param q: Caudal.
    :param w: Diámetro.

    :return: Altura de velocidad en metros
    """
    return (8 * pow(q, 2)) / (9.8 * math.pow(math.pi, 2) * math.pow(w, 4))


def calculate_friction(e, d):
    """
    Calcula la fricción a partir del espesor y el diametro
    :param e:
    :param d:
    :return:
    """
    return 0.25 / math.pow(math.log10(float(d) / e) + 0.56820172, 2)


def calculate_k_derivac(q, qo, qsigue=True):
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


def calculate_b(pv, e, f, d, w, qe, q, pc, lar, l, zc, m, pent=0.5):
    """
    Calcula la altura de agua de la bomba B.

    :param pv: Presion de vapor
    :param e: Parametro de error asociado a presion de vapor
    :param f: friccion en tuberia
    :param d: Diametro de riego (diametro de alcance)
    :param w: Diametro de tuberia
    :param qe: Caudal de entrada
    :param q: Caudal de salida por cada rama
    :param pc: Perdidas de codo
    :param lar: Largo de tuberia antes de sistema
    :param l: Cantidad de ramas
    :param zc: altura del rio
    :param m: Largo de la tuberia gruesa
    :param pent: Perdida entrada
    :return:
    """

    # Sumatoria por perdidas en friccion
    fper = 0.0
    sf = f * float(m - d / 2) / (l * w)  # Perdida por friccion
    for i in range(1, l):
        qit = qe - i * q  # Caudal en cada tramo del tubo por friccion
        sder = calculate_k_derivac(qe - i * q, qe + q * (1 - i))  # Derivación
        fper += (sf + sder) * alt_vel(qit, w)

    fper_prev = pc + pent + lar * f / w  # Factor de perdida para tuberia L
    b = -zc + pv * (1 + e) + fper + fper_prev * alt_vel(qe, w)
    return b
