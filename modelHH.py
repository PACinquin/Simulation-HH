# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -----------------------------------------------------------------------------
# Modèle Hudgkin & Huxley
# 2015  Pierre-Antoine Cinquin
#
# Nécessite :
#  - Python 2.7.x
#  - Numpy 1.10.1 ou plus
#  - Matplotlib 1.5.0 ou plus
# -----------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np

##### FONCTIONS #####
# Calcul des alphas en fonction de V

def alpha_h(U):
    return 0.07 * np.exp(-U/20.)

def alpha_m(U):
    return 0.1*(25.-U)/((np.exp((25.-U)/10.)) -1.)

def alpha_n(U):
    return 0.01*(10.-U) / ((np.exp((10.-U)/10.))-1.)

# Calcul des bêtas en fonction de V

def beta_h(U):
    return 1./(np.exp((30.-U)/10.)+1.)

def beta_m(U):
    return 4.* np.exp(-U/18.)

def beta_n(U):
    return 0.125 * np.exp(-U/80.)
	
#Calcul de la probabilité d'ouverture
def proba_ouverture(alpha, x, beta):
    return (alpha * ( 1 - x )) - (beta * x)
	
#Fonction modèle Hodgkin Huxley
def hh(Tmax, I=1, dt=0.010, C=1.):
    for t in range(1,int(Tmax/dt)):
	#on calcule les proba d'ouverture des canaux
        dpn = dt * proba_ouverture(alpha_n(V[t-1]), n[t-1], beta_n(V[t-1]))
        dpm = dt * proba_ouverture(alpha_m(V[t-1]), m[t-1], beta_m(V[t-1]))
        dph = dt * proba_ouverture(alpha_h(V[t-1]), h[t-1], beta_h(V[t-1]))
	#on calcule le changement de concentration en Na et K
        dK = (gK * ((n[t-1])**4.) * (V[t-1] - EK))
        dNa = (gNa * (m[t-1])**3. * (h[t-1]) * (V[t-1]-ENa))
        K.append(dK)
        Na.append(dNa)
	#Equation du modèle de Hodgkin&Huxley
        dV = dt * (I - ((gL * (V[t-1] - EL)) + K[t-1] + Na[t-1]))/C
        n.append(n[t-1] + dpn)
        m.append(m[t-1] + dpm)
        h.append(h[t-1] + dph)
        V.append(V[t-1] + dV)
        tps.append(tps[t-1] + dt)
    return tps,V,K,Na,n,m,h 
	
##### CONSTANTES #####
EL = 10.6
gL = 0.3
gK = 36.
EK = -12.
gNa = 120.
ENa = 115.
    
# On stocke les résultats dans des vecteurs
tps = [0.]
V=[0.]
m=[0.]
n = [0.]
h = [1.]
K = [0.]
Na = [0.]

##### MAIN #####
t2, V2, lK, lNa, n2, m2, h2 = hh(30.)

# Pour commencer à -65mV
#for _ in range(len(V2)):
#	V2[_] -= 65

# Affichage des résultats

plt.plot(t2, V2, label = 'V')
plt.legend()
plt.plot(t2, lNa, label = 'I,Na')
plt.plot(t2, lK, label = 'I,K')
plt.legend()
plt.plot(t2,n2, label = 'n')
plt.plot(t2,m2, label = 'm')
plt.plot(t2,h2, label = 'h')
plt.legend()
plt.show()
\ No newline at end of file
