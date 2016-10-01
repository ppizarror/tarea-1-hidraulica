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
dk = getDiametern(N, DMAX, DMIN)
dl = getDiametern(M, DMAX, DMIN)
d = get_final_d_solution(dk, dl)

# Se obtienen valores
k = d[v][1]  # Parámetro k
l = d[v][2]  # Parámetro l
diam = d[v][0]  # Diámetro

# Se obtiene consumo por regaderos
consumohora_por_regadero = 3600 * getConsumoCaudalRegadio(C, diam)
consumohora_total = k * l * consumohora_por_regadero
fhrs = getConsumoConMinimoRegadero(consumohora_por_regadero, CAUDALES_RIEGO[v])
precio_regaderos = getPreciosRegaderos(diam) * k * l

# Caudal de entrada máximo e mínimo
qe_min = round(CAUDALES_RIEGO[v][1] * k * l / 3600, 3)
qe_max = round(CAUDALES_RIEGO[v][0] * k * l / 3600, 3)

# Caudal por cada rama
q_min = round(CAUDALES_RIEGO[v][1] * k / 3600, 3)
q_max = round(CAUDALES_RIEGO[v][0] * k / 3600, 3)
radio = R

# Se calcula el reynolds para qmin y qmax
reynolds_min = calculo_reynolds(qe_min, W)
reynolds_max = calculo_reynolds(qe_max, W)

# Se calcula el coeficiente de pérdida para la curva
kc_min = calcular_coef_curva(qe_min, W, radio)
kc_max = calcular_coef_curva(qe_max, W, radio)

# Se obtiene el total de tuberías
total_tub_peq = getCantTuberiaFromD(d, v, L)[0]
total_tub_grand = getCantTuberiaFromD(d, v, L)[1]
precio_tub_peq = 0
precio_tub_grand = W_PRECIO * total_tub_grand

# Costo total
costo_total = precio_tub_grand + precio_tub_peq + precio_regaderos

#
# Se imprime el estado del plot
#
for di in range(0, len(d)):
    print di, getAreaResidual(N, M, d[di][0], d[di][1], d[di][2])
for di in range(0, len(d)):
    print di, d[di][0], getCantTuberiaFromD(d, di, L)

print '\nSolución elegida: {0}'.format(v)
print 'Diametro: {0}m'.format(diam)
print 'k: {0}'.format(k)
print 'l: {0}'.format(l)

print '\nTuberias pequeñas: {0}m'.format(total_tub_peq)
print 'Tuberias gruesas: {0}m'.format(total_tub_grand)
print 'Regaderos totales: {0}'.format(k * l)

print '\nCosto tuberias pequeñas: {0}$'.format(addComa(precio_tub_peq))
print 'Costo tuberias grandes: {0}$'.format(addComa(precio_tub_grand))
print 'Costo regaderos: {0}$'.format(addComa(precio_regaderos))
print 'Costo total: {0}$'.format(addComa(costo_total))

print '\nConsumo por regadero: {0} m3/s = {1} m3/h'.format(
    getConsumoCaudalRegadio(C, diam), consumohora_por_regadero)
print 'Consumo agua total: {0} m3/h'.format(consumohora_total)
print 'El sistema debe funcionar entre {1}, {0} horas a caudales Qe {2} m3/s y ' \
      '{3} m3/s respectivamente'.format(fhrs[0], fhrs[1], qe_min, qe_max)

print LINEBAR
print 'Valores variables:'
print '\tRadio curvatura inicial: {0}m'.format(radio)
print '\tFriccion f: {0}'.format(F)
print '\tDiametro tuberia gruesa: {0}mm'.format(W)
print '\tCaudales por rama q [min, max]: {0} m3/s\t {1} m3/s'.format(q_min,
                                                                     q_max)
print '\tCaudales entrada qe [min, max]: {0}m'.format(qe_min, qe_max)
print '\tReynolds [min, max]: {0} \t {1}'.format(reynolds_min, reynolds_max)
print '\tCoeficiente perdida curva {2}m: {0} \t {1}'.format(kc_min, kc_max,
                                                            radio),
print LINEBAR

# Se calcula b para el caudal mínimo
calculate_b(10, GAMMA, 1, F, diam, W, qe_min, q_min, kc_min, L, l, ZC, M)

# Se plotea
plot_solution(d, v, not False)
