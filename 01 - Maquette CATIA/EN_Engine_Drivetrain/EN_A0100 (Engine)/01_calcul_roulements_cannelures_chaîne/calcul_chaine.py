import numpy as np
import matplotlib.pyplot as plt
from math import pi
from scipy.optimize import fsolve, fmin, curve_fit
from scipy.interpolate import RegularGridInterpolator

#%% Calculs chaîne de transmission secondaire

#%% Chaînes [pas,masse linéique, charge rupture]

B08B=[12.7,0.68,17800]
B10B=[15.875,0.85,22200]
B12B=[19.05,1.16,28900]

#%% Calcul

chain=B10B

p=chain[0]/1000
M=chain[1]
Frup=chain[2]

#Pignon & moteur
C=240
Z=13
omega_max=5500*2*pi/60

#Couronne
Zc=round(3.23*Z)

#%% Géométrie

alpha=2*pi/Z
phi=pi*(1/6-1/Z)
Dp = p/np.sin(pi/Z)

e=0.2
L=2*e+p*(Z+Zc)/2+p**2/e*((Z-Zc)/(2*pi))**2

#%% Dynamique
Fu= 2*C/Dp
Fc= M*(Dp*omega_max/2)**2

N = [100*i for i in range(60)]
P = []
for i in range(60):
    P.append(((Fu*60/(p*Z*N[i]*2*(pi/60)))+M*(Dp*N[i]*2*pi/120)**2)*N[i]*2*(pi/60) - M*(N[i]*2*(pi/60))**3)
    
plt.plot(N, P)

indice=np.array(range(1,Z))

F=(Fu+Fc)*(np.sin(phi)/np.sin(alpha+phi))**indice
G=(Fu+Fc)*(np.sin(phi)/np.sin(alpha+phi))**(indice-1)*(np.sin(alpha)/np.sin(alpha+phi))

GX=G*np.cos(phi-alpha*(indice-1/2))
GZ=G*np.sin(-phi+alpha*(indice-1/2))

Krup=Frup/(Fu+Fc)

#%% Coefficients de sécurité (d'après Chaînes mécaniques - Techniques de l'ingénieur)

K1=19/Z
K2=1
K3=120*p/L
K4=1.1
K5=1

K=K1*K2*K3*K4*K5
