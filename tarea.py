# coding=utf-8
"""
Se imprimen estados para cada una de las soluciones
"""

# Se importan funciones
from funciones import *
from graph import plot_solution
from const import *
from tuberias import *

# Constantes
C = 1e-7  # Consumo m/s por unidad de Area
CAUDALES_RIEGO = [[2.3, 10.8], [1.6, 2.2], [1.0, 1.2], [0.45, 0.72]]
dpeq = 0.75 * PULGD  # Diámetro tubería pequeña
e = 0.2  # Porcentaje de error en la presión de vapor
KL = 2  # Perdida curva 90 grados
ZC = -10  # Cota del rio

# Se escoge tubería
ww = 1
W = TUBERIAS[ww]
W_PRECIO = TUBERIAS_PRECIOS[ww]

# Se calcula la fricción
F = calculate_friction(ESPESOR, W * 1000)

# Solución elegida
v = 3

# Se obtienen soluciones de diámetros
dk = get_diametern(N, DMAX, DMIN)
dl = get_diametern(M, DMAX, DMIN)
d = get_final_d_solution(dk, dl)

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
qe_min = round(CAUDALES_RIEGO[v][1] * k * l / 3600, 3)
qe_max = round(CAUDALES_RIEGO[v][0] * k * l / 3600, 3)

# Caudal por cada rama
q_min = round(CAUDALES_RIEGO[v][1] * k / 3600, 3)
q_max = round(CAUDALES_RIEGO[v][0] * k / 3600, 3)
radio = R

# Se calcula el reynolds para qmin y qmax
reynolds_min = round(calculo_reynolds(qe_min, W), 1)
reynolds_max = round(calculo_reynolds(qe_max, W), 1)

# Se calcula el coeficiente de pérdida para la curva
kc_min = round(calcular_coef_curva(qe_min, W, radio), 3)
kc_max = round(calcular_coef_curva(qe_max, W, radio), 3)

# Se obtiene el total de tuberías
total_tub_peq = get_cant_tuberia_from_d(d, v, L)[0]
total_tub_grand = get_cant_tuberia_from_d(d, v, L)[1]
precio_tub_peq = 0
precio_tub_grand = W_PRECIO * total_tub_grand

# Costo total
costo_total = precio_tub_grand + precio_tub_peq + precio_regaderos

# Calculo de la bomba grande requerida
b_min = calculate_b(10, 1, F, diam, W, qe_min, q_min, kc_min, L, l, ZC, M)
b_max = calculate_b(10, 1, F, diam, W, qe_max, q_max, kc_max, L, l, ZC, M)
b_min = round(b_min, 3)
b_max = round(b_max, 3)

#
# Se imprime el estado del plot
#
for di in range(0, len(d)):
    print di, get_area_residual(N, M, d[di][0], d[di][1], d[di][2])
for di in range(0, len(d)):
    print di, d[di][0], get_cant_tuberia_from_d(d, di, L)

print '\nSolución elegida: {0}'.format(v)
print 'Diametro: {0}m'.format(diam)
print 'k: {0}'.format(k)
print 'l: {0}'.format(l)

print '\nTuberias pequeñas: {0}m'.format(total_tub_peq)
print 'Tuberias gruesas: {0}m'.format(total_tub_grand)
print 'Regaderos totales: {0}'.format(k * l)

print '\nCosto tuberias pequeñas: {0}$'.format(add_coma(precio_tub_peq))
print 'Costo tuberias grandes: {0}$'.format(add_coma(precio_tub_grand))
print 'Costo regaderos: {0}$'.format(add_coma(precio_regaderos))
print 'Costo total: {0}$'.format(add_coma(costo_total))

print '\nConsumo por regadero: {0} m3/s = {1} m3/h'.format(
    get_consumo_caudal_regadio(C, diam), consumohora_por_regadero)
print 'Consumo agua total: {0} m3/h'.format(consumohora_total)
print 'El sistema debe funcionar entre {1}, {0} horas a caudales Qe {2} m3/s' \
      ' y {3} m3/s respectivamente'.format(fhrs[0], fhrs[1], qe_min, qe_max)

print LINEBAR
print 'Valores variables:'
print '\tRadio curvatura inicial: {0}m'.format(radio)
print '\tFriccion f:\t\t\t\t {0}'.format(round(F, 5))
print '\tDiametro tuberia gruesa: {0}mm'.format(W)
print '\n\tTiempos funcionamiento:  {0}h\t\t {1}h'.format(fhrs[1], fhrs[0])
print '\tCaudales por rama q:\t {0} m3/s\t {1} m3/s'.format(q_min,
                                                            q_max)
print '\tCaudales entrada qe:\t {0} m3/s\t {1} m3/s'.format(
    qe_min, qe_max)
print '\tReynolds: \t\t\t\t {0} \t {1}'.format(reynolds_min,
                                               reynolds_max)
print '\tCoeficiente curva {2}m:\t {0} \t \t {1}'.format(kc_min, kc_max,
                                                         radio)
print '\tAltura bomba grande:\t {0} \t {1}'.format(b_min, b_max)

# Se plotea
plot_solution(d, v, False)
