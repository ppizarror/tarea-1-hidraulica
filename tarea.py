# coding=utf-8
"""
Se imprimen estados para cada una de las soluciones
"""

# Se importan funciones
from funciones import *
from graph import plot_solution
from const import *
from tuberias import *
import sys

# Constantes
C = 1e-7  # Consumo m/s por unidad de Area
CAUDALES_RIEGO = [[2.3, 10.8], [1.6, 2.2], [1.0, 1.2], [0.45, 0.72]]
dpeq = 0.75 * PULGD  # Diámetro tubería pequeña
e = 0.2  # Porcentaje de error en la presión de vapor
KL = 2  # Pérdida curva 90 grados
KREG = 0.1  # Pérdida en regaderos
KVALV = 0.25
ZC = -10  # Cota del rio
PV = 10  # Presión de vapor
PRECIO_VALVULA = 44437

# Se obtienen soluciones de diámetros
dk = get_diametern(N, DMAX, DMIN)
dl = get_diametern(M, DMAX, DMIN)
d = get_final_d_solution(dk, dl)

print 'Soluciones diámetros:'
for di in range(0, len(d)):
    print '\t', di + 1, d[di][0], get_cant_tuberia_from_d(d, di, L)

# Se eligen soluciones
ww = 1  # Tubería grande
wp = 0  # Tubería pequeña

# Se crea cada solución
for v in range(4):
    # Se redirige el print a un archivo de texto
    sys.stdout = open('solucion {0}/resultados solucion {0}.txt'.format(v +
                                                                        1),
                      'w')

    # Se escoge tubería grande
    W = TUBERIAS[ww]
    W_PRECIO = TUBERIAS_PRECIOS[ww]
    WP = TUBERIAS[wp]
    WP_PRECIO = TUBERIAS_PRECIOS[wp]

    # Se calcula la fricción
    F = calculate_friction(ESPESOR, W * 1000)

    # Se obtienen valores
    k = d[v][1]  # Parámetro k
    l = d[v][2]  # Parámetro l
    diam = d[v][0]  # Diámetro

    # Se obtiene consumo por regaderos
    consumohora_por_regadero = 3600 * get_consumo_caudal_regadio(C, diam)
    consumohora_total = k * l * consumohora_por_regadero
    fhrs = get_consumo_con_minimo_regadero(consumohora_por_regadero,
                                           CAUDALES_RIEGO[v])
    precio_regaderos = get_precios_regaderos(diam) * k * l

    # Caudal de entrada máximo e mínimo
    qe_min = round(CAUDALES_RIEGO[v][1] * k * l / 3600, 5)
    qe_max = round(CAUDALES_RIEGO[v][0] * k * l / 3600, 5)

    # Caudal por cada rama
    q_min = round(CAUDALES_RIEGO[v][1] * k / 3600, 5)
    q_max = round(CAUDALES_RIEGO[v][0] * k / 3600, 5)
    radio = R

    # Se calcula el reynolds para qmin y qmax
    reynolds_min = round(calculo_reynolds(qe_min, W), 1)
    reynolds_max = round(calculo_reynolds(qe_max, W), 1)

    # Se calcula el coeficiente de pérdida para la curva
    kc_min = round(calcular_coef_curva(qe_min, W, radio), 4)
    kc_max = round(calcular_coef_curva(qe_max, W, radio), 4)

    # Se obtiene el total de tuberías
    total_tub_peq = get_cant_tuberia_from_d(d, v, L)[0]
    total_tub_grand = get_cant_tuberia_from_d(d, v, L)[1]
    precio_tub_peq = WP_PRECIO * total_tub_peq
    precio_tub_grand = W_PRECIO * total_tub_grand

    # Precio de las válvulas
    precio_valv = PRECIO_VALVULA * l

    # Costo total
    costo_total = precio_tub_grand + precio_tub_peq + precio_regaderos
    costo_total += precio_valv

    # Calculo de la bomba grande requerida
    b_min = calculate_b(PV, e, F, diam, W, qe_min, q_min, kc_min, L, l, ZC,
                        M)
    b_max = calculate_b(PV, e, F, diam, W, qe_max, q_max, kc_max, L, l, ZC,
                        M)
    b_min = round(b_min, 3)
    b_max = round(b_max, 3)

    # Cálculo de la bomba más grande de las pequeñas
    bp_min = calculate_min_b(PV, e, F, diam, W, WP, qe_min, q_min, kc_min,
                             L, l, k, ZC, M, N, b_min, KREG, KVALV, v + 1,
                             'tmin')
    bp_max = calculate_min_b(PV, e, F, diam, W, WP, qe_max, q_max, kc_max,
                             L, l, k, ZC, M, N, b_max, KREG, KVALV, v + 1,
                             'tmax')
    bp_min = round(bp_min, 3)
    bp_max = round(bp_max, 3)

    #
    # Se imprime el estado del plot
    #
    print 'Solución elegida:'
    print '\tDiámetro alcance regador: {0}\t({1} m)'.format(v + 1, diam)
    print '\tTubería gruesa elegida:   {0}\t({1} mm)'.format(ww, W)
    print '\tTubería peq. elegida:     {0}\t({1} mm)'.format(wp, WP)
    print '\tk:\t\t\t  {0}'.format(k)
    print '\tl:\t\t\t  {0}'.format(l)

    print LINEBAR
    print 'Materiales:'
    print '\tDiámetro riego:\t\t {0} m'.format(diam)
    print '\tTuberías pequeñas:\t {0} m'.format(total_tub_peq)
    print '\tTuberías gruesas:\t {0} m'.format(total_tub_grand)
    print '\tDiámetro tubería gruesa: {0} mm'.format(W)
    print '\tDiámetro tubería peq.:   {0} mm'.format(WP)
    print '\tRegaderos totales:\t {0}'.format(k * l)
    print '\n\tCosto tuberías pequeñas: $ {0}'.format(
        add_coma(precio_tub_peq))
    print '\tCosto tuberías grandes:\t $ {0}'.format(
        add_coma(precio_tub_grand))
    print '\tCosto regaderos:\t $ {0}'.format(add_coma(precio_regaderos))
    print '\tCosto válvulas:\t\t $ {0}'.format(add_coma(precio_valv))
    print '\tCosto total:\t\t $ {0}'.format(add_coma(costo_total))

    print LINEBAR
    print 'Valores de la solución:'
    print '\tCota del rio:           {0} m'.format(ZC)
    print '\tRadio curv. inicial:     {0} m'.format(radio)
    print '\tFricción f:              {0}'.format(round(F, 5))
    print '\tCoef. pérdida regador:   {0}'.format(KREG)
    print '\tCoef. pérdida válvulas:  {0}'.format(KVALV)
    print '\tParámetro de error e:    {0}'.format(e)
    print '\tKPSH:                    {0} m'.format(PV * (1 + e))

    print '\n\tConsumo por regadero:\t {0} m3/s -> {1} m3/h'.format(
        get_consumo_caudal_regadio(C, diam), consumohora_por_regadero)
    print '\tConsumo agua total:\t {0} m3/h'.format(consumohora_total)
    print '\n\tTiempos funcionamiento:  {0} h\t\t {1} h'.format(fhrs[1],
                                                                fhrs[0])
    print '\tCaudales por rama Q:\t {0} m3/s\t {1} m3/s'.format(q_min,
                                                                q_max)
    print '\tCaudales entrada Qe:\t {0} m3/s\t {1} m3/s'.format(
        qe_min, qe_max)
    print '\tReynolds: \t\t {0} \t {1}'.format(reynolds_min, reynolds_max)
    print '\tCoeficiente curva {2} m:\t {0} \t {1}'.format(kc_min, kc_max,
                                                              radio)
    print '\tAltura bomba grande:\t {0} m \t {1} m'.format(b_min, b_max)
    print '\tAltura bomba pequeña:\t {0} m \t {1} m'.format(bp_min, bp_max)

    # Se plotea
    plot_solution(d, v, v + 1)

    # Se cierra el print
    sys.stdout.close()
